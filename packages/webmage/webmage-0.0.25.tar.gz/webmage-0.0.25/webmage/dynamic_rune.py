from .support import style_attributes
from .dynamic_rune_array import DynamicRuneArr
from selenium.common.exceptions import StaleElementReferenceException

class DynamicRune:
    def __init__(self, selenium_rune, driver):
        self.selenium_rune = selenium_rune
        self.driver = driver
        self.text = selenium_rune.text

    def __repr__(self):
        return f'{self.outerHTML}'

    def __str__(self):
        return f'{self.outerHTML}'

    def __getitem__(self, item_request):
        value = self.selenium_rune.get_attribute(item_request)
        return value

    def __contains__(self, item_request):
        value = self.selenium_rune.get_attribute(item_request)
        return value

    def cast_js(self, javaScript, arguments=None):
        return self.driver.execute_script(javaScript, arguments)

    def select(self, css_selector):
        return DynamicRune(self.selenium_rune.find_element_by_css_selector(css_selector), self.driver)

    def selectAll(self, css_selector):
        return DynamicRuneArr([*[DynamicRune(i, self.driver) for i in self.selenium_rune.find_elements_by_css_selector(css_selector)]])

    def get_attributes(self):
        self.attributes = {}
        for attribute in self.selenium_rune.get_property('attributes'):
            self.attributes[attribute['nodeName']] = self.selenium_rune.get_attribute(attribute['nodeName'])

    def click(self):
        self.selenium_rune.click()


    def destroy(self, css_selector=None):
        # If no css_selector is provided, then delete the element itself.
        if css_selector == None:
            self.cast_js("""
            arguments[0].remove();
            """, self.selenium_rune)        
        # If a css_selector is provided, then search for an element within the element to delete.
        else:
            self.cast_js(f"""
            let els = arguments[0].querySelectorAll('{css_selector}');
            els.length > 0 ? els[0].remove() : null;
            """, self.selenium_rune)

    def destroyAll(self, css_selector):
        self.cast_js(f"""
        arguments[0].querySelectorAll('{css_selector}')
            .forEach(el => el.remove());
        """, self.selenium_rune)

