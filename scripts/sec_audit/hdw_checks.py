# SecurityCheck class and _ (i18n function) are dynamically injected by the main script.


class CheckHDW01(SecurityCheck):
    check_id = "HDW-01"

    def audit(self):
        return False, _("HDW-01_manual")


class CheckHDW02(SecurityCheck):
    check_id = "HDW-02"

    def audit(self):
        return False, _("HDW-02_manual")


class CheckHDW03(SecurityCheck):
    check_id = "HDW-03"

    def audit(self):
        return False, _("HDW-03_manual")


class CheckHDW04(SecurityCheck):
    check_id = "HDW-04"

    def audit(self):
        return False, _("HDW-04_manual")


class CheckHDW05(SecurityCheck):
    check_id = "HDW-05"

    def audit(self):
        return False, _("HDW-05_manual")


class CheckHDW06(SecurityCheck):
    check_id = "HDW-06"

    def audit(self):
        return False, _("HDW-06_manual")


class CheckHDW07(SecurityCheck):
    check_id = "HDW-07"

    def audit(self):
        return False, _("HDW-07_manual")


class CheckHDW08(SecurityCheck):
    check_id = "HDW-08"

    def audit(self):
        return False, _("HDW-08_manual")
