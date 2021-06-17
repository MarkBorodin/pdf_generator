import time

from selenium import webdriver


class TestBasic(object):
    """tests for pdf generator"""

    # general
    driver = None
    sleep = 1
    login_url = 'http://localhost/admin/login/?next=/admin/'

    # general results
    check_template = None
    check_client_address = None
    check_client_name = None
    check_email = None
    check_description = None
    check_signature = None
    check_payment_information = None
    check_category = None
    check_bemerkung = None
    check_page_number = None
    check_page_template = None
    check_phase_name = None
    check_designations_name = None
    check_designations_description = None
    check_designations_price = None
    check_designations_quantity = None
    create_by_template = None

    # general data
    client_address = 'Brovary'
    client_name = 'Mark'
    email = 'mark@mail.com'
    description = 'description test description'
    signature = 'mark'
    payment_information = 'CHF'
    category = 'SEO'
    bemerkung = ''
    page = ''
    phase = ''
    designations_name = 'designations_name_1'
    designations_description = 'designations_description_1'
    designations_price = '1000'
    designations_quantity = '1'
    number = None
    link = None
    offer_number_created_by_template = None

    # offer
    offer_add_url = 'http://localhost/admin/pdf_generator/offer/add/'
    offer_all_url = 'http://localhost/admin/pdf_generator/offer/'
    offer_created_by_template_link = None

    # results offer
    offer_created = None
    offer_deleted = None

    # invoice
    invoice_all_url = 'http://localhost/admin/pdf_generator/invoice/'

    # results invoice
    invoice_create = None

    # offer_confirmation
    offer_confirmation_all_url = 'http://localhost/admin/pdf_generator/offerconfirmation/'

    # results offer_confirmation
    offer_confirmation_create = None

    # template
    template_add_url = 'http://localhost/admin/pdf_generator/template/add/'
    template_all_url = 'http://localhost/admin/pdf_generator/template/'
    template_name = 'template test'
    template_number = None

    # results template
    template_create = None
    template_deleted = None


    def __init__(self, username: str, password: str) -> None: # noqa
        self.username = username
        self.password = password

    def get_connection(self) -> None:
        """selenium driver connection chrome"""
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.headless = False
            self.driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
        except Exception as e:
            print(f'get_connection: {e}')

    def login(self) -> None:
        """login to the admin panel. You need to specify a username and password in self.username and self.password"""
        try:
            self.driver.get(self.login_url)
            self.driver.find_element_by_id('id_username').send_keys(self.username)
            self.driver.find_element_by_id('id_password').send_keys(self.password)
            self.driver.find_element_by_xpath('//*[@id="login-form"]/div[3]/input').click()
        except Exception as e:
            print(f'login: {e}')

    def close_connection(self) -> None:
        """close connection"""
        self.driver.close()
        self.driver.quit()

    def test_offer_create(self) -> None:
        """creating an offer"""
        try:
            self.driver.get(self.offer_add_url)
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_client_name').send_keys(self.client_name)
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_client_address').send_keys(self.client_address)
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_email').send_keys(self.email)
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_description').send_keys(self.description)
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_bemerkung').send_keys(self.bemerkung)
            time.sleep(self.sleep)
            [elemet for elemet in self.driver.find_element_by_id('id_payment_information').find_elements_by_tag_name('option') if elemet.text == self.payment_information][0].click() # noqa
            time.sleep(self.sleep)
            [elemet for elemet in self.driver.find_element_by_id('id_signature').find_elements_by_tag_name('option') if elemet.text == self.signature][0].click() # noqa
            time.sleep(self.sleep)
            [elemet for elemet in self.driver.find_element_by_id('id_category').find_elements_by_tag_name('option') if elemet.text == self.category][0].click() # noqa
            time.sleep(self.sleep)
            self.driver.find_element_by_xpath('//*[@id="pages-group"]/div/fieldset/table/tbody[2]/tr/td/a').click()
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_pages-0-number').send_keys(self.page)
            time.sleep(self.sleep)
            self.driver.find_element_by_xpath('//*[@id="pages-0-phases-group"]/div/fieldset/table/tbody[2]/tr/td/a').click() # noqa
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_pages-0-phases-0-name').send_keys(self.phase)
            time.sleep(self.sleep)
            self.driver.find_element_by_xpath('//*[@id="pages-0-phases-0-designations-group"]/div/fieldset/table/tbody[2]/tr/td/a').click() # noqa
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_pages-0-phases-0-designations-0-name').send_keys(self.designations_name) # noqa
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_pages-0-phases-0-designations-0-description').send_keys(self.designations_description) # noqa
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_pages-0-phases-0-designations-0-price').send_keys(self.designations_price) # noqa
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_pages-0-phases-0-designations-0-quantity').send_keys(self.designations_quantity) # noqa
            time.sleep(self.sleep)
            self.driver.find_element_by_name('_save').click()
            if self.driver.current_url == self.offer_all_url:
                self.offer_created = True
            else:
                self.offer_created = False
            self.offer_number = self.driver.find_elements_by_class_name('field-number')[0].text
            self.offer_link = self.offer_all_url + self.offer_number + '/change/'
        except Exception as e:
            print(f'test_offer_create: {e}')

    def test_del_offer(self) -> None:
        """deleting an offer"""
        try:
            self.driver.get(self.offer_all_url)
            time.sleep(self.sleep)
            self.driver.find_elements_by_class_name('action-select')[0].click()
            time.sleep(self.sleep)
            [elemet for elemet in self.driver.find_element_by_class_name('actions').find_elements_by_tag_name('option') if elemet.text == 'Delete selected Offerten'][0].click() # noqa
            time.sleep(self.sleep)
            self.driver.find_element_by_xpath('//*[@id="changelist-form"]/div[1]/button').click()
            time.sleep(self.sleep)
            self.driver.find_element_by_xpath('//*[@id="content"]/form/div/input[4]').click()
            time.sleep(self.sleep)
            if self.driver.find_element_by_class_name('success').text == 'Successfully deleted 1 Offerte.':
                self.offer_deleted = True
            else:
                self.offer_deleted = False
        except Exception as e:
            print(f'test_del_offer: {e}')

    def test_del_template(self) -> None:
        """deleting template"""
        try:
            self.driver.get(self.template_all_url)
            time.sleep(self.sleep)
            self.driver.find_elements_by_class_name('action-select')[0].click()
            time.sleep(self.sleep)
            [elemet for elemet in self.driver.find_element_by_class_name('actions').find_elements_by_tag_name('option') if elemet.text == 'Delete selected Vorlagen'][0].click() # noqa
            time.sleep(self.sleep)
            self.driver.find_element_by_xpath('//*[@id="changelist-form"]/div[1]/button').click()
            time.sleep(self.sleep)
            self.driver.find_element_by_xpath('//*[@id="content"]/form/div/input[4]').click()
            time.sleep(self.sleep)
            if self.driver.find_element_by_class_name('success').text == 'Successfully deleted 1 Vorlage.':
                self.template_deleted = True
            else:
                self.template_deleted = False
        except Exception as e:
            print(f'test_del_template: {e}')

    def test_check_offer_or_template(self, link) -> None:
        """check the correctness of the data in the offer or template"""
        self.driver.get(link)
        time.sleep(self.sleep)

        try:
            if self.driver.find_element_by_xpath('//*[@id="offer_form"]/div/fieldset/div[1]/div/div').text == '-':
                self.check_template = True
            else:
                self.check_template = False
        except Exception as e:
            print(f'check_template: {e}')

        try:
            if self.driver.find_element_by_id('id_client_address').text == self.client_address:
                self.check_client_address = True
            else:
                self.check_client_address = False
        except Exception as e:
            print(f'check_client_address: {e}')

        try:
            if self.driver.find_element_by_id('id_client_name').text == self.client_name:
                self.check_client_name = True
            else:
                self.check_client_name = False
        except Exception as e:
            print(f'check_client_name: {e}')

        try:
            if self.driver.find_element_by_id('id_email').text == self.email:
                self.check_email = True
            else:
                self.offer_check_email = False
        except Exception as e:
            print(f'check_email: {e}')

        try:
            if self.driver.find_element_by_id('id_description').text == self.description:
                self.check_description = True
            else:
                self.check_description = False
        except Exception as e:
            print(f'check_description: {e}')

        try:
            if self.driver.find_element_by_id('id_bemerkung').text == self.bemerkung:
                self.check_bemerkung = True
            else:
                self.check_bemerkung = False
        except Exception as e:
            print(f'check_bemerkung: {e}')

        try:
            if self.payment_information in self.driver.find_element_by_id('id_payment_information').text: # noqa
                self.check_payment_information = True
            else:
                self.check_payment_information = False
        except Exception as e:
            print(f'check_payment_information: {e}')

        try:
            if self.signature in self.driver.find_element_by_id('id_signature').text:
                self.check_signature = True
            else:
                self.check_signature = False
        except Exception as e:
            print(f'check_signature: {e}')

        try:
            if self.category in self.driver.find_element_by_id('id_category').text:
                self.check_category = True
            else:
                self.check_category = False
        except Exception as e:
            print(f'check_category: {e}')

        try:
            if self.driver.find_element_by_xpath('//*[@id="id_pages-0-number"]').get_attribute('value') == self.page + '1': # noqa
                self.check_page_number = True
            else:
                self.check_page_number = False
        except Exception as e:
            print(f'check_page_number: {e}')

        try:
            if self.driver.find_element_by_xpath('//*[@id="pages-0"]/tr[1]/td[3]/p').text == '-':
                self.check_page_template = True
            else:
                self.check_page_template = False
        except Exception as e:
            print(f'check_page_template: {e}')

        try:
            if self.driver.find_element_by_id('id_pages-0-phases-0-name').text == 'phase' + self.phase:
                self.check_phase_name = True
            else:
                self.check_phase_name = False
        except Exception as e:
            print(f'check_phase_name: {e}')

        try:
            if self.driver.find_element_by_id('id_pages-0-phases-0-designations-0-name').text == self.designations_name: # noqa
                self.check_designations_name = True
            else:
                self.check_designations_name = False
        except Exception as e:
            print(f'offer_check_designations_name: {e}')

        try:
            if self.driver.find_element_by_id('id_pages-0-phases-0-designations-0-description').text == self.designations_description: # noqa
                self.check_designations_description = True
            else:
                self.check_designations_description = False
        except Exception as e:
            print(f'check_designations_description: {e}')

        try:
            if self.driver.find_element_by_id('id_pages-0-phases-0-designations-0-price').get_attribute('value') == self.designations_price + '0.0': # noqa
                self.check_designations_price = True
            else:
                self.check_designations_price = False
        except Exception as e:
            print(f'check_designations_price: {e}')

        try:
            if self.driver.find_element_by_id('id_pages-0-phases-0-designations-0-quantity').get_attribute('value') == '1' + self.designations_quantity: # noqa
                self.check_designations_quantity = True
            else:
                self.check_designations_quantity = False
        except Exception as e:
            print(f'check_designations_quantity: {e}')

    def test_create_invoice(self, of_number: str) -> None:
        try:
            """checking invoice creation"""
            self.driver.get(self.offer_all_url)
            if self.driver.find_element_by_xpath('//*[@id="result_list"]/tbody/tr[1]/th/a').text == of_number:
                self.driver.find_element_by_xpath('//*[@id="result_list"]/tbody/tr[1]/td[8]/a').click()
            self.driver.get(self.invoice_all_url)
            time.sleep(self.sleep)
            if self.driver.find_element_by_xpath('//*[@id="result_list"]/tbody/tr[1]/th/a').text == of_number:
                self.invoice_create = True
            else:
                self.invoice_create = False
        except Exception as e:
            print(f'test_create_invoice: {e}')

    def test_create_offer_confirmation(self, of_number: str) -> None:
        try:
            """checking offer_confirmation creation"""
            self.driver.get(self.offer_all_url)
            if self.driver.find_element_by_xpath('//*[@id="result_list"]/tbody/tr[1]/th/a').text == of_number:
                self.driver.find_element_by_xpath('//*[@id="result_list"]/tbody/tr[1]/td[9]/a').click()
            self.driver.get(self.offer_confirmation_all_url)
            time.sleep(self.sleep)
            if self.driver.find_element_by_xpath('//*[@id="result_list"]/tbody/tr[1]/th/a').text == of_number:
                self.offer_confirmation_create = True
            else:
                self.offer_confirmation_create = False
        except Exception as e:
            print(f'test_create_offer_confirmation: {e}')

    def test_template_create(self) -> None:
        """creating template"""
        try:
            self.driver.get(self.template_add_url)
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_name').send_keys(self.template_name)
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_client_name').send_keys(self.client_name)
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_client_address').send_keys(self.client_address)
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_email').send_keys(self.email)
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_description').send_keys(self.description)
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_bemerkung').send_keys(self.bemerkung)
            time.sleep(self.sleep)
            [elemet for elemet in self.driver.find_element_by_id('id_payment_information').find_elements_by_tag_name('option') if elemet.text == self.payment_information][0].click() # noqa
            time.sleep(self.sleep)
            [elemet for elemet in self.driver.find_element_by_id('id_signature').find_elements_by_tag_name('option') if elemet.text == self.signature][0].click() # noqa
            time.sleep(self.sleep)
            [elemet for elemet in self.driver.find_element_by_id('id_category').find_elements_by_tag_name('option') if elemet.text == self.category][0].click() # noqa
            time.sleep(self.sleep)
            self.driver.find_element_by_xpath('//*[@id="pages-group"]/div/fieldset/table/tbody[2]/tr/td/a').click()
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_pages-0-number').send_keys(self.page)
            time.sleep(self.sleep)
            self.driver.find_element_by_xpath('//*[@id="pages-0-phases-group"]/div/fieldset/table/tbody[2]/tr/td/a').click() # noqa
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_pages-0-phases-0-name').send_keys(self.phase)
            time.sleep(self.sleep)
            self.driver.find_element_by_xpath('//*[@id="pages-0-phases-0-designations-group"]/div/fieldset/table/tbody[2]/tr/td/a').click() # noqa
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_pages-0-phases-0-designations-0-name').send_keys(self.designations_name) # noqa
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_pages-0-phases-0-designations-0-description').send_keys(self.designations_description) # noqa
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_pages-0-phases-0-designations-0-price').send_keys(self.designations_price) # noqa
            time.sleep(self.sleep)
            self.driver.find_element_by_id('id_pages-0-phases-0-designations-0-quantity').send_keys(self.designations_quantity) # noqa
            time.sleep(self.sleep)
            self.driver.find_element_by_name('_save').click()
            if self.driver.current_url == self.template_all_url:
                self.template_create = True
            else:
                self.template_create = False
            self.template_number = self.driver.find_elements_by_class_name('field-number')[0].text
            self.template_link = self.template_all_url + self.template_number + '/change/'
        except Exception as e:
            print(f'test_template_create: {e}')

    def test_offer_create_by_template(self) -> None:
        """creating an offer by template"""
        try:
            self.driver.get(self.offer_add_url)
            time.sleep(self.sleep)
            [elemet for elemet in self.driver.find_element_by_id('id_template').find_elements_by_tag_name('option') if elemet.text == self.template_name][0].click()  # noqa
            self.driver.find_element_by_name('_save').click()
            if 'successfully' in self.driver.find_element_by_class_name('success').text:
                self.offer_create_by_template = True
            else:
                self.offer_create_by_template = False
            time.sleep(self.sleep)
            self.offer_number_created_by_template = self.driver.find_element_by_class_name('success').find_element_by_tag_name('a').text # noqa
            self.offer_created_by_template_link = self.offer_all_url + self.offer_number_created_by_template + '/change/' # noqa
        except Exception as e:
            print(f'test_offer_create_by_template: {e}')

    def results_offer_create(self) -> None:
        """show results"""
        print('______________')
        print('CREATE OFFER')
        print('______________')
        print(f'test_offer_create: {self.offer_created}')

    def results_check_data(self) -> None:
        """results_check_data"""
        print('______________')
        print('CHECK DATA')
        print('______________')
        print(f'test_check_template: {self.check_template}')
        print(f'test_client_address: {self.check_client_address}')
        print(f'test_check_client_name: {self.check_client_name}')
        print(f'test_check_email: {self.check_email}')
        print(f'test_check_description: {self.check_description}')
        print(f'test_check_signature: {self.check_signature}')
        print(f'test_check_payment_information: {self.check_payment_information}')
        print(f'test_check_category: {self.check_category}')
        print(f'test_check_bemerkung: {self.check_bemerkung}')
        print(f'test_check_page_number: {self.check_page_number}')
        print(f'test_check_page_template: {self.check_page_template}')
        print(f'test__check_phase_name: {self.check_phase_name}')
        print(f'test_check_designations_name: {self.check_designations_name}')
        print(f'test_check_designations_description: {self.check_designations_description}')
        print(f'test_check_designations_price: {self.check_designations_price}')
        print(f'test_check_designations_quantity: {self.check_designations_quantity}')

    def results_invoice_create(self) -> None:
        """results_invoice_create"""
        print('______________')
        print('CREATE INVOICE')
        print('______________')
        print(f'test_invoice_create: {self.invoice_create}')

    def results_offer_confirmation_create(self) -> None:
        """results_offer_confirmation_create"""
        print('______________')
        print('CREATE OFFER_CONFORMATION')
        print('______________')
        print(f'test_offer_confirmation_create: {self.offer_confirmation_create}')

    def results_offer_delete(self) -> None:
        """results_offer_delete"""
        print('______________')
        print('DELETE OFFER')
        print('______________')
        print(f'test_del_offer: {self.offer_deleted}')

    def results_template_create(self) -> None:
        """results_template_create"""
        print('______________')
        print('CREATE TEMPLATE')
        print('______________')
        print(f'test_template_create: {self.template_create}')

    def results_offer_create_by_template(self) -> None:
        """results_offer_create_by_template"""
        print('______________')
        print('CREATE OFFER BY TEMPLATE')
        print('______________')
        print(f'test_offer_create_by_template: {self.offer_create_by_template}')

    def results_template_delete(self) -> None:
        """results template delete"""
        print('______________')
        print('DELETE TEMPLATE')
        print('______________')
        print(f'test_del_template: {self.template_deleted}')


if __name__ == '__main__':
    # get username and password
    username = 'mark'
    password = '52970130'
    sleep = 1

    print("START TESTS")
    # _______________________________________________________________________________________________________________
    print('********************************************************************************************************')
    # _____________________________Create and check offer____________________________________________________________

    # create object
    test_object = TestBasic(username, password)
    time.sleep(sleep)

    # get connection
    test_object.get_connection()
    time.sleep(sleep)

    # login
    test_object.login()
    time.sleep(sleep)

    # creating an offer
    test_object.test_offer_create()
    time.sleep(sleep)

    # check the correctness of the data in the offer
    test_object.test_check_offer_or_template(test_object.offer_link)
    time.sleep(sleep)

    # show results
    test_object.results_offer_create()
    test_object.results_check_data()
    time.sleep(sleep)

    # close connection
    test_object.close_connection()
    time.sleep(sleep)

    # get offer number for next check
    offer_number = test_object.offer_number
    time.sleep(sleep)

    # _______________________________________________________________________________________________________________
    print('********************************************************************************************************')
    # ______________________________Create and check invoice and offer_confirmation__________________________________

    # create object
    test_object = TestBasic(username, password)
    time.sleep(sleep)

    # get connection
    test_object.get_connection()
    time.sleep(sleep)

    # login
    test_object.login()
    time.sleep(sleep)

    # checking invoice creation
    test_object.test_create_invoice(offer_number)
    time.sleep(sleep)

    # offer confirmation creation
    test_object.test_create_offer_confirmation(offer_number)
    time.sleep(sleep)

    # show results
    test_object.results_invoice_create()
    test_object.results_offer_confirmation_create()
    time.sleep(sleep)

    # close connection
    test_object.close_connection()
    time.sleep(sleep)

    # _______________________________________________________________________________________________________________
    print('********************************************************************************************************')
    # _______________________________________________Delete offer (invoice and offer_confirmation)___________________

    # create object
    test_object = TestBasic(username, password)
    time.sleep(sleep)

    # get connection
    test_object.get_connection()
    time.sleep(sleep)

    # login
    test_object.login()
    time.sleep(sleep)

    # deleting an offer
    test_object.test_del_offer()
    time.sleep(sleep)

    # show results
    test_object.results_offer_delete()
    time.sleep(sleep)

    # close connection
    test_object.close_connection()
    time.sleep(sleep)

    # _______________________________________________________________________________________________________________
    print('********************************************************************************************************')
    # _______________________________________________Create, check template__________________________________________

    # create object
    test_object = TestBasic(username, password)
    time.sleep(sleep)

    # get connection
    test_object.get_connection()
    time.sleep(sleep)

    # login
    test_object.login()
    time.sleep(sleep)

    # template creation
    test_object.test_template_create()
    time.sleep(sleep)

    # check the correctness of the data in the template
    test_object.test_check_offer_or_template(test_object.template_link)
    time.sleep(sleep)

    # show results
    test_object.results_template_create()
    test_object.results_check_data()
    time.sleep(sleep)

    # close connection
    test_object.close_connection()
    time.sleep(sleep)

    # _______________________________________________________________________________________________________________
    print('********************************************************************************************************')
    # _______________________Create, check (delete at the end) offer based on the template___________________________

    # create object
    test_object = TestBasic(username, password)
    time.sleep(sleep)

    # get connection
    test_object.get_connection()
    time.sleep(sleep)

    # login
    test_object.login()
    time.sleep(sleep)

    # create offer by template
    test_object.test_offer_create_by_template()
    time.sleep(sleep)

    # check the correctness of the data in the offer created by template
    test_object.test_check_offer_or_template(test_object.offer_created_by_template_link)
    time.sleep(sleep)

    # show results
    test_object.results_offer_create_by_template()
    test_object.results_check_data()
    time.sleep(sleep)

    # deleting test offer
    test_object.test_del_offer()

    # close connection
    test_object.close_connection()
    time.sleep(sleep)

    # _______________________________________________________________________________________________________________
    print('********************************************************************************************************')
    # ________________________________________________Delete template________________________________________________

    # create object
    test_object = TestBasic(username, password)
    time.sleep(sleep)

    # get connection
    test_object.get_connection()
    time.sleep(sleep)

    # login
    test_object.login()
    time.sleep(sleep)

    # delete template
    test_object.test_del_template()
    time.sleep(sleep)

    # show results
    test_object.results_template_delete()
    time.sleep(sleep)

    # close connection
    test_object.close_connection()
    time.sleep(sleep)

    # _______________________________________________________________________________________________________________
    print('********************************************************************************************************')
    # _______________________________________________________________________________________________________________
    print("END TESTS")
