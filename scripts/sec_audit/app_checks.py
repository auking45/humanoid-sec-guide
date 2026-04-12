# SecurityCheck class and _ (i18n function) are dynamically injected by the main script.


class CheckAPP01(SecurityCheck):
    check_id = "APP-01"

    def audit(self):
        return False, _("APP-01_manual")


class CheckAPP02(SecurityCheck):
    check_id = "APP-02"

    def audit(self):
        # Check if tpm2-tools or softhsm2 packages, required for hardware signature verification, are installed
        success, _ = self.run_cmd("dpkg -l | grep -E 'tpm2-tools|softhsm2'")
        if success:
            return True, _("APP-02_pass")
        else:
            return False, _("APP-02_fail")


class CheckAPP03(SecurityCheck):
    check_id = "APP-03"

    def audit(self):
        return False, _("APP-03_manual")


class CheckAPP04(SecurityCheck):
    check_id = "APP-04"

    def audit(self):
        # Check if fail2ban is active for API rate limiting and flood prevention
        success, _ = self.run_cmd("systemctl is-active fail2ban")
        if success:
            return True, _("APP-04_pass")
        else:
            return False, _("APP-04_fail")


class CheckAPP05(SecurityCheck):
    check_id = "APP-05"

    def audit(self):
        return False, _("APP-05_manual")


class CheckAPP06(SecurityCheck):
    check_id = "APP-06"

    def audit(self):
        return False, _("APP-06_manual")


class CheckAPP07(SecurityCheck):
    check_id = "APP-07"

    def audit(self):
        return False, _("APP-07_manual")
