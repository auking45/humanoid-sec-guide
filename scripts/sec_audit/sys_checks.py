# SecurityCheck class and _ (i18n function) are dynamically injected by the main script.


class CheckSYS01(SecurityCheck):
    check_id = "SYS-01"
    def audit(self):
        return False, _("SYS-01_manual")


class CheckSYS02(SecurityCheck):
    check_id = "SYS-02"
    def audit(self):
        return False, _("SYS-02_manual")


class CheckSYS03(SecurityCheck):
    check_id = "SYS-03"
    def audit(self):
        return False, _("SYS-03_manual")


class CheckSYS04(SecurityCheck):
    check_id = "SYS-04"
    def audit(self):
        return False, _("SYS-04_manual")


class CheckSYS05(SecurityCheck):
    check_id = "SYS-05"
    def audit(self):
        return False, _("SYS-05_manual")


class CheckSYS06(SecurityCheck):
    check_id = "SYS-06"
    def audit(self):
        success, out = self.run_cmd("mount | grep ' / '")
        if success and " ro," in out:
            return True, _("SYS-06_pass")
        else:
            return False, _("SYS-06_fail")


class CheckSYS07(SecurityCheck):
    check_id = "SYS-07"
    def audit(self):
        success, out = self.run_cmd("cat /proc/cmdline")
        if success and "nokaslr" not in out:
            return True, _("SYS-07_pass")
        else:
            return False, _("SYS-07_fail")


class CheckSYS08(SecurityCheck):
    check_id = "SYS-08"
    def audit(self):
        return False, _("SYS-08_manual")


class CheckSYS09(SecurityCheck):
    check_id = "SYS-09"
    def audit(self):
        return False, _("SYS-09_manual")


class CheckSYS10(SecurityCheck):
    check_id = "SYS-10"

    def audit(self):
        success, _ = self.run_cmd("which gcc")
        if not success:
            return True, _("SYS-10_pass")
        else:
            return False, _("SYS-10_fail")


class CheckSYS28(SecurityCheck):
    check_id = "SYS-28"

    def audit(self):
        success, out = self.run_cmd("modprobe -c | grep 'blacklist usb-storage'")
        if success and "blacklist usb-storage" in out:
            return True, _("SYS-28_pass")
        else:
            return False, _("SYS-28_fail")


class CheckSYS11(SecurityCheck):
    check_id = "SYS-11"
    def audit(self):
        return False, _("SYS-11_manual")


class CheckSYS12(SecurityCheck):
    check_id = "SYS-12"
    def audit(self):
        return False, _("SYS-12_manual")


class CheckSYS13(SecurityCheck):
    check_id = "SYS-13"
    def audit(self):
        return False, _("SYS-13_manual")


class CheckSYS14(SecurityCheck):
    check_id = "SYS-14"
    def audit(self):
        return False, _("SYS-14_manual")


class CheckSYS15(SecurityCheck):
    check_id = "SYS-15"
    def audit(self):
        return False, _("SYS-15_manual")


class CheckSYS16(SecurityCheck):
    check_id = "SYS-16"
    def audit(self):
        return False, _("SYS-16_manual")


class CheckSYS17(SecurityCheck):
    check_id = "SYS-17"
    def audit(self):
        return False, _("SYS-17_manual")


class CheckSYS18(SecurityCheck):
    check_id = "SYS-18"
    def audit(self):
        return False, _("SYS-18_manual")


class CheckSYS19(SecurityCheck):
    check_id = "SYS-19"
    def audit(self):
        return False, _("SYS-19_manual")


class CheckSYS20(SecurityCheck):
    check_id = "SYS-20"
    def audit(self):
        return False, _("SYS-20_manual")


class CheckSYS21(SecurityCheck):
    check_id = "SYS-21"
    def audit(self):
        return False, _("SYS-21_manual")


class CheckSYS22(SecurityCheck):
    check_id = "SYS-22"
    def audit(self):
        success, out = self.run_cmd("aa-status | grep 'apparmor module is loaded'")
        if success:
            return True, _("SYS-22_pass")
        else:
            return False, _("SYS-22_fail")


class CheckSYS23(SecurityCheck):
    check_id = "SYS-23"
    def audit(self):
        return False, _("SYS-23_manual")


class CheckSYS24(SecurityCheck):
    check_id = "SYS-24"
    def audit(self):
        return False, _("SYS-24_manual")


class CheckSYS27(SecurityCheck):
    check_id = "SYS-27"
    def audit(self):
        success, out = self.run_cmd("sysctl net.ipv4.ip_forward")
        if success and "net.ipv4.ip_forward = 0" in out:
            return True, _("SYS-27_pass")
        else:
            return False, _("SYS-27_fail")


class CheckSYS29(SecurityCheck):
    check_id = "SYS-29"

    def audit(self):
        success, out = self.run_cmd(
            "sshd -T | grep -E '^(permitrootlogin|passwordauthentication)'"
        )
        if (
            "permitrootlogin no" in out.lower()
            and "passwordauthentication no" in out.lower()
        ):
            return True, _("SYS-29_pass")
        else:
            return False, _("SYS-29_fail")

class CheckSYS30(SecurityCheck):
    check_id = "SYS-30"
    def audit(self):
        return False, _("SYS-30_manual")

class CheckSYS31(SecurityCheck):
    check_id = "SYS-31"
    def audit(self):
        return False, _("SYS-31_manual")
