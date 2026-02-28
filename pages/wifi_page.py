class WifiPage:
    def __init__(self, page):
        self.page = page
        self.ssid_input = page.locator('input[name="ssid_2g"]') # Thay selector thực tế
        self.save_button = page.locator('button#apply-wifi')

    def change_ssid(self, new_ssid):
        self.ssid_input.clear()
        self.ssid_input.fill(new_ssid)
        self.save_button.click()
        self.page.wait_for_load_state("networkidle")
