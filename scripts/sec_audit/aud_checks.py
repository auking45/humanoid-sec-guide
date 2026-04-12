# SecurityCheck class and _ (i18n function) are dynamically injected by the main script.


class CheckAUD01(SecurityCheck):
    check_id = "AUD-01"

    def audit(self):
        success, _ = self.run_cmd("systemctl is-active auditd")
        if success:
            return True, _("AUD-01_pass")
        else:
            return False, _("AUD-01_fail")


class CheckAUD02(SecurityCheck):
    check_id = "AUD-02"

    def audit(self):
        return False, _("AUD-02_manual")


class CheckAUD03(SecurityCheck):
    check_id = "AUD-03"

    def audit(self):
        return False, _("AUD-03_manual")


class CheckAUD04(SecurityCheck):
    check_id = "AUD-04"

    def audit(self):
        return False, _("AUD-04_manual")


class CheckAUD05(SecurityCheck):
    check_id = "AUD-05"

    def audit(self):
        return False, _("AUD-05_manual")


class CheckAUD06(SecurityCheck):
    check_id = "AUD-06"

    def audit(self):
        return False, _("AUD-06_manual")


class CheckAUD07(SecurityCheck):
    check_id = "AUD-07"

    def audit(self):
        return False, _("AUD-07_manual")


class CheckAUD08(SecurityCheck):
    check_id = "AUD-08"

    def audit(self):
        return False, _("AUD-08_manual")


class CheckAUD09(SecurityCheck):
    check_id = "AUD-09"

    def audit(self):
        return False, _("AUD-09_manual")


class CheckAUD10(SecurityCheck):
    check_id = "AUD-10"

    def audit(self):
        return False, _("AUD-10_manual")


class CheckAUD11(SecurityCheck):
    check_id = "AUD-11"

    def audit(self):
        return False, _("AUD-11_manual")


class CheckAUD12(SecurityCheck):
    check_id = "AUD-12"

    def audit(self):
        return False, _("AUD-12_manual")
