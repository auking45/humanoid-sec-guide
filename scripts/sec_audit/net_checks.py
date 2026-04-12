# SecurityCheck class and _ (i18n function) are dynamically injected by the main script.


class CheckCOM01(SecurityCheck):
    check_id = "COM-01"

    def audit(self):
        return False, _("COM-01_manual")


class CheckCOM02(SecurityCheck):
    check_id = "COM-02"

    def audit(self):
        return False, _("COM-02_manual")


class CheckCOM03(SecurityCheck):
    check_id = "COM-03"

    def audit(self):
        return False, _("COM-03_manual")


class CheckCOM04(SecurityCheck):
    check_id = "COM-04"

    def audit(self):
        return False, _("COM-04_manual")


class CheckCOM05(SecurityCheck):
    check_id = "COM-05"

    def audit(self):
        return False, _("COM-05_manual")


class CheckCOM06(SecurityCheck):
    check_id = "COM-06"

    def audit(self):
        return False, _("COM-06_manual")


class CheckCOM07(SecurityCheck):
    check_id = "COM-07"

    def audit(self):
        return False, _("COM-07_manual")


class CheckCOM08(SecurityCheck):
    check_id = "COM-08"

    def audit(self):
        return False, _("COM-08_manual")


class CheckCOM09(SecurityCheck):
    check_id = "COM-09"

    def audit(self):
        # WireGuard 모듈이 로드되어 있거나 wg 네트워크 인터페이스가 존재하는지 확인
        success, _ = self.run_cmd(
            "ip link show type wireguard || lsmod | grep -q wireguard"
        )
        if success:
            return True, _("COM-09_pass")
        else:
            return False, _("COM-09_fail")


class CheckCOM10(SecurityCheck):
    check_id = "COM-10"

    def audit(self):
        return False, _("COM-10_manual")


class CheckCOM11(SecurityCheck):
    check_id = "COM-11"

    def audit(self):
        return False, _("COM-11_manual")


class CheckCOM12(SecurityCheck):
    check_id = "COM-12"

    def audit(self):
        return False, _("COM-12_manual")


class CheckCOM13(SecurityCheck):
    check_id = "COM-13"

    def audit(self):
        return False, _("COM-13_manual")


class CheckCOM14(SecurityCheck):
    check_id = "COM-14"

    def audit(self):
        return False, _("COM-14_manual")


class CheckLOC01(SecurityCheck):
    check_id = "LOC-01"

    def audit(self):
        return False, _("LOC-01_manual")


class CheckLOC02(SecurityCheck):
    check_id = "LOC-02"

    def audit(self):
        return False, _("LOC-02_manual")


class CheckLOC03(SecurityCheck):
    check_id = "LOC-03"

    def audit(self):
        return False, _("LOC-03_manual")


class CheckLOC04(SecurityCheck):
    check_id = "LOC-04"

    def audit(self):
        return False, _("LOC-04_manual")


class CheckLOC05(SecurityCheck):
    check_id = "LOC-05"

    def audit(self):
        return False, _("LOC-05_manual")


class CheckLOC06(SecurityCheck):
    check_id = "LOC-06"

    def audit(self):
        return False, _("LOC-06_manual")


class CheckLOC07(SecurityCheck):
    check_id = "LOC-07"

    def audit(self):
        return False, _("LOC-07_manual")


class CheckLOC08(SecurityCheck):
    check_id = "LOC-08"

    def audit(self):
        success, out = self.run_cmd("ufw status")
        if success and "Status: active" in out:
            return True, _("LOC-08_pass")
        else:
            return False, _("LOC-08_fail")


class CheckLOC09(SecurityCheck):
    check_id = "LOC-09"

    def audit(self):
        return False, _("LOC-09_manual")


class CheckLOC10(SecurityCheck):
    check_id = "LOC-10"

    def audit(self):
        return False, _("LOC-10_manual")
