# -*- coding: utf-8 -*-

# Implementation of the "Warenpost International ReST-API"
#
# This is a completely different interface that Deutsche Post came up many years
# after the "1C4A" Internetmarke API.  For some strange reason they didn't
# extend the old Internetmarke API to add support for the harmonized label and
# the electronic customs declaration.  Instead, they decided to implement a
# completely different API with different standards (REST vs. SOAP) with
# literally nothing in common to the old Internetmarke API

import json
import logging
import hashlib
from datetime import datetime

import requests
from lxml import etree
from pytz import timezone

_logger = logging.getLogger(__name__)

class WarenpostInt(object):
    """Represents the Warenpost Internatoinal ReST interface."""
    def __init__(self, partner_id, key, ekp, pk_email, pk_passwd, key_phase="1", sandbox = False):
        self.sandbox = sandbox
        self.partner_id = 'DP_LT' if sandbox else partner_id
        self.key = key
        self.ekp = ekp
        self.key_phase = '1' if sandbox else key_phase
        self.pk_email = pk_email
        self.pk_passwd = pk_passwd
        if sandbox:
            self.auth_url = 'https://api-qa.deutschepost.com/v1'
            self.url = 'https://api-qa.deutschepost.com/dpi/shipping/v1'
        else:
            self.auth_url = 'https://api.deutschepost.com/v1'
            self.url = 'https://api.deutschepost.com/dpi/shipping/v1'
        self.user_token = None
        self.wallet_balance = None

    # FIXME: merge with inema?
    @staticmethod
    def compute_1c4a_hash(partner_id, req_ts, key_phase, key):
        """ Compute 1C4A request hash accordig to Section 4 of service description. """
        # trim leading and trailing spaces of each argument
        partner_id = partner_id.strip()
        req_ts = req_ts.strip()
        key_phase = key_phase.strip()
        key = key.strip()
        # concatenate with "::" separator
        inp = "%s::%s::%s::%s" % (partner_id, req_ts, key_phase, key)
        # compute MD5 hash as 32 hex nibbles
        md5_hex = hashlib.md5(inp.encode('utf8')).hexdigest()
        # return the first 8 characters
        return md5_hex[:8]

    # FIXME: merge with inema?
    @staticmethod
    def gen_timestamp():
        """Generate a timestamp as used in the Warenpsost International API."""
        de_zone = timezone("Europe/Berlin")
        de_time = datetime.now(de_zone)
        return de_time.strftime("%d%m%Y-%H%M%S")

    def gen_headers(self):
        """Generate the HTTP headers required for the API."""
        ret = {
            'KEY_PHASE': self.key_phase,
            'PARTNER_ID': self.partner_id,
            'Authorization': 'Bearer %s' % self.user_token
            }
        if self.sandbox:
            ret['REQUEST_TIMESTAMP'] = '16082018-122210'
            ret['PARTNER_SIGNATURE'] = '9d7c35be'
        else:
            timestamp = self.gen_timestamp()
            sig = self.compute_1c4a_hash(self.partner_id, timestamp, self.key_phase, self.key)
            ret['REQUEST_TIMESTAMP'] = timestamp
            ret['PARTNER_SIGNATURE'] = sig
        return ret

    def get_token(self):
        """Get an Access Token for further API requests."""
        url = "%s/%s" % (self.auth_url, 'auth/accesstoken')
        auth = requests.auth.HTTPBasicAuth(self.pk_email, self.pk_passwd)
        ret = requests.request('GET', url, headers=self.gen_headers(), auth=auth)
        et = etree.XML(ret.content)
        e_user_token = et.find(".//{http://oneclickforapp.dpag.de/V3}userToken")
        e_wallet_balance = et.find(".//{http://oneclickforapp.dpag.de/V3}walletBalance")
        # update status + return token
        self.user_token = e_user_token.text
        self.wallet_balance = e_wallet_balance.text
        _logger.debug("User Token: %s", self.user_token)
        _logger.info("Wallet balance: %s", self.wallet_balance)
        return e_user_token.text

    def request(self, method, suffix, json=None, headers=None):
        """Wrapper for issuing HTTP requests against the API.
           This internally generates all required headers, including Authorization."""
        url = "%s/%s" % (self.url, suffix)
        # FIXME: automatically ensure we have a [current] user_token
        h = headers.copy() if headers else {}
        h.update(self.gen_headers())
        _logger.debug("HTTP Request: %s %s: HDR: %s JSON: %s", method, url, h, json)
        r = requests.request(method, url, json=json, headers=h)
        _logger.debug("HTTP Response: %s", r.content)
        return r

    class Address(object):
        """Common Representation of a postal address.  In their infinite cluelessness,
           the developes of the Warenpost International API decided it's a good idea to
           use a flat, non-hierarchical structure with different names of fields for
           sender and recipient."""
        def __init__(self, name, addr_lines, city, country_code, postal_code='', state=None,
                     phone=None, fax=None, email=None):
            if len(name) > 30:
                raise ValueError('Maximum length of name is 30 chars')
            if len(addr_lines) > 3:
                raise ValueError('Maximum number of 3 Address Lines supported')
            if len(city) > 30:
                raise ValueError('Maximum length of city is 30 chars')
            if len(country_code) != 2:
                raise ValueError('Country must be 2-digit ISO-3166-1 code')
            if state and len(state) > 20:
                raise ValueError('Maximum length of state is 20 chars')
            if phone and len(phone) > 15:
                raise ValueError('Maximum length of phone number is 15 chars')
            if fax and len(fax) > 15:
                raise ValueError('Maximum length of fax number is 15 chars')
            if email and len(email) > 50:
                raise ValueError('Maximum length of email address is 50 chars')
            for l in addr_lines:
                if len(l) > 40:
                    raise ValueError('Maximum length of address lines is 40 chars')
            self.name = name
            self.addr_lines = addr_lines
            self.city = city
            self.postal_code = postal_code
            self.country_code = country_code
            self.state = state
            self.phone = phone
            self.fax = fax
            self.email = email

        def as_sender(self):
            """Represent an Address object as JSON fields of a sender."""
            if len(self.addr_lines) > 2:
                raise ValueError('Maximum number of 2 Address Lines supported')
            for l in self.addr_lines:
                if len(l) > 30:
                    raise ValueError('Maximum length of address lines is 30 chars')
            ret = {
                'senderName': self.name,
                'senderAddressLine1': self.addr_lines[0],
                'senderAddressLine2': self.addr_lines[1] if len(self.addr_lines) > 1 else '',
                'senderCity': self.city,
                'senderPostalCode': self.postal_code,
                'senderCountry': self.country_code,
                }
            if self.phone:
                ret['senderPhone'] = self.phone
            if self.email:
                ret['senderEmail'] = self.email
            return ret

        def as_recipient(self):
            """Represent an Address object as JSON fields of a sender."""
            ret = {
                'recipient': self.name,
                'addressLine1': self.addr_lines[0],
                'city': self.city,
                'postalCode': self.postal_code,
                'destinationCountry': self.country_code,
                }
            if len(self.addr_lines) > 1:
                ret['addressLine2'] = self.addr_lines[1]
                if len(self.addr_lines) > 2:
                    ret['addressLine3'] = self.addr_lines[2]
            if self.state:
                ret['state'] = self.state
            if self.phone:
                ret['recipientPhone'] = self.phone
            if self.fax:
                ret['recipientFax'] = self.fax
            if self.email:
                ret['recipientEmail'] = self.email
            return ret

    def build_content_item(self, line_weight_g, line_value, qty, hs_code=None, origin_cc=None,
                           desc=None):
        """Build an 'content item' in the language of the WaPoInt API. Represents one
           line on the customs form."""
        line_weight_g = int(line_weight_g)
        if line_weight_g > 2000:
            raise ValueError('Maximum line weight is 2000g')
        qty = int(qty)
        if qty > 99 or qty < 1:
            raise ValueError('Maximum line quantity is 99')
        if desc and len(desc) > 33:
            raise ValueError('Maximum length of contentPieceDescription is 33 chars')
        if hs_code and (len(hs_code) < 4 or len(hs_code) > 10):
            raise ValueError('HS-Code must be between 4 and 10 characters long')
        ret = {
            'contentPieceNetweight': line_weight_g,
            'contentPieceValue': "%.2f" % (line_value),
            'contentPieceAmount': qty,
            }
        if hs_code:
            ret['contentPieceHsCode'] = str(hs_code)
        if desc:
            ret['contentPieceDescription'] = str(desc)
        if origin_cc:
            ret['contentPieceOrigin'] = origin_cc
        return ret

    def shrink_contents_if_needed(self, contents):
        """Attempt to shrink the number of content lines below the permitted 5. We
           intentionally ignore the country of origin and group all lines by the
           HTS code. All lines sharing the same HTS code are merged to one,
           hopefully this is sufficient to get the count below 5."""
        if len(contents) < 5:
            return contents
        # group items by HTS code
        by_hts = {}
        for c in contents:
            hts = c['contentPieceHsCode'].strip()
            if hts in by_hts:
                by_hts[hts].append(c)
            else:
                by_hts[hts] = [c]
        if len(by_hts.keys()) > 5:
            raise ValueError('More than 5 distinct HTS numbers(%u); cannot merge' % (len(by_hts.keys())))
        out = []
        # generate one aggregate item per HTS code
        for k in by_hts:
            total_grams = 0
            total_value = 0
            total_qty = 0
            for c in by_hts[k]:
                total_grams += c['contentPieceNetweight']
                total_value += float(c['contentPieceValue'])
                total_qty += c['contentPieceAmount']
            aggregate = by_hts[k][0]
            aggregate['contentPieceAmount'] = total_qty
            aggregate['contentPieceValue'] = "%.2f" % (total_value)
            aggregate['contentPieceNetweight'] = total_grams
            out.append(aggregate)
        return out

    def build_item(self, product, sender, recipient, weight_grams, amount=0, currency='EUR',
                   shipment_nature='SALE_GOODS', customer_reference=None, contents=None):
        """Build an 'item' in the language of the WaPoInt API. Represents one shipment."""
        weight_grams = int(weight_grams)
        if weight_grams > 2000:
            raise ValueError('Maximum item gross weight is 2000g')
        if len(currency) != 3:
            raise ValueError('Currency must be expressed as 3-digit ISO-4217 code')
        if contents and len(contents) > 5:
            raise ValueError('Custom Contents must not contain more than 5 lines')
        ret = {
            'product': str(product),
            'serviceLevel': 'STANDARD',
            'shipmentAmount': int(amount),
            'shipmentCurrency': currency,
            'shipmentGrossWeight': weight_grams,
            'shipmentNaturetype': shipment_nature,
            }
        # merge in the sender and recipient fields
        ret.update(sender.as_sender())
        ret.update(recipient.as_recipient())
        if contents:
            ret['contents'] = contents
        if customer_reference:
            customer_reference = str(customer_reference)
            if len(customer_reference) > 20:
                raise ValueError('Maximum length of customer reference is 20 chars')
            ret['custRef'] = customer_reference
        return ret

    def build_order(self, items, contact_name, order_status='FINALIZE'):
        """Build an 'order' in the language of the WaPoInt API.  Consists of multiple shipments."""
        ret = {
            'customerEkp': self.ekp,
            'orderStatus': order_status,
            'paperwork': {
                'contactName': contact_name,
                'awbCopyCount': 1,
                },
            'items': items
            }
        return ret

    def api_create_order(self, items, contact_name, order_status='FINALIZE'):
        """Issue an API request to create an order consisting of items."""
        order = self.build_order(items, contact_name=contact_name, order_status=order_status)
        _logger.info("Order Request: %s", order)
        r = self.request('POST', 'orders', json = order)
        # TODO: figure out the AWB and the (item, barcode, voucherId, ...) for the items
        json_resp = r.json()
        #print(json.dumps(json_resp, indent=4))
        _logger.info("Order Response: %s", json_resp)
        # TODO: download the PDF for each AWB
        return json_resp

    def api_get_item_label(self, item_id, accept='application/pdf'):
        """Download the label for a given item.  Returns PDF as 'bytes'"""
        r = self.request('GET', 'items/%s/label' % item_id, headers={'Accept': accept})
        return r.content

    def api_get_item_labels(self, awb, accept='application/pdf'):
        """Download the labels for all items in a given AWB. Returns PDF as 'bytes'"""
        r = self.request('GET', 'shipments/%s/itemlabels' % awb, headers={'Accept': accept})
        return r.content
