import time
from unittest import TestCase

from aws.cert import generate_self_signed_cert, import_cert, delete_cert, generate_and_import_self_signed, get_certs, \
    get_cert_arn, get_certificate
from aws.region import get_acm
import warnings


class TestCertificateManager(TestCase):

    @classmethod
    def setUpClass(cls):
        # Hide boto3 warnings. This is a known issue with boto3 + unittest.
        warnings.simplefilter('ignore', category=ResourceWarning)

    def test_self_signed(self):
        c = generate_self_signed_cert('test.simoncomputing.com', 'US', 'Virginia', 'Alexandria', 'SimonComputing', 2)
        self.assertIsNotNone(c['private'])
        self.assertIsNotNone(c['public'])
        delete_cert('test.simoncomputing.com')

    def test_import_self_signed(self):
        try:
            c = generate_self_signed_cert('unittest1234.simoncomputing.com', 'US', 'Virginia', 'Alexandria',
                                          'SimonComputing', 2)
            arn = import_cert('unittest1234.simoncomputing.com', c['public'], c['private'], {'lol': 'tag'})
            check_exists = get_cert_arn('unittest1234.simoncomputing.com')
            if not check_exists:
                self.fail('cert does not exist!')
            tags = get_acm().list_tags_for_certificate(CertificateArn=arn).get('Tags', [])
            for tag in tags:
                if tag.get('Key') == 'lol':
                    self.assertEqual('tag', tag.get('Value'))
                elif tag.get('Key') == 'Name':
                    self.assertEqual('unittest1234.simoncomputing.com', tag.get('Value'))
        except:
            self.fail('cert not imported!')
        finally:
            delete_cert('unittest1234.simoncomputing.com')

    def test_gen_import_self_signed(self):
        try:
            arn = generate_and_import_self_signed('unittest1234.simoncomputing.com', 'unittest1234.simoncomputing.com',
                                                  'US', 'Virginia', 'Alexandria', 'SimonComputing', 2)
            get_acm().get_certificate(CertificateArn=arn)
        except:
            self.fail('cert not imported!')
        finally:
            delete_cert('unittest1234.simoncomputing.com')

    def test_get_certs(self):
        try:
            pre_list = get_certs()
            found = False
            for cert in pre_list:
                if cert['DomainName'] == 'unittestgetcerts.simoncomputing.com':
                    found = True
            self.assertFalse(found)
            c = generate_self_signed_cert('unittestgetcerts.simoncomputing.com', 'US', 'Virginia', 'Alexandria',
                                          'SimonComputing', 2)
            import_cert('unittestgetcerts.simoncomputing.com', c['public'], c['private'])
            time.sleep(10)
            post_list = get_certs()
            found = False
            for cert in post_list:
                if cert['DomainName'] == 'unittestgetcerts.simoncomputing.com':
                    found = True
            self.assertTrue(found)
        finally:
            delete_cert('unittestgetcerts.simoncomputing.com')

    def test_delete_cert(self):
        try:
            c = generate_self_signed_cert('unittestdeletecert.simoncomputing.com', 'US', 'Virginia', 'Alexandria',
                                          'SimonComputing', 2)
            import_cert('unittestdeletecert.simoncomputing.com', c.get('public', 'N/A'), c.get('private', 'N/A'))
            time.sleep(10)
            pre_list = get_certs()
            found = False
            for cert in pre_list:
                if cert['DomainName'] == 'unittestdeletecert.simoncomputing.com':
                    found = True
            self.assertTrue(found)

            did_delete = delete_cert('unittestdeletecert.simoncomputing.com')
            self.assertTrue(did_delete)
            time.sleep(10)
            post_list = get_certs()

            for cert in post_list:
                if cert['DomainName'] == 'unittestdeletecert.simoncomputing.com':
                    self.fail('found cert after deleting')
        finally:
            delete_cert('unittestdeletecert.simoncomputing.com')

    def test_delete_bad_cert(self):
        self.assertFalse(delete_cert('THISCERTDOESNOTEXIST'))

    def test_get_bad_cert_arn(self):
        self.assertFalse(get_cert_arn('THISCERTDOESNOTEXIST'))

    def test_get_certificate_no_domain(self):
        with self.assertRaisesRegex(AssertionError, 'requires domain_name'):
            get_certificate('')

    def test_get_certificate_no_match(self):
        test_domain = 'unittest4321.simoncomputing.com'
        result = get_certificate(test_domain)
        self.assertEqual(0, len(result))
