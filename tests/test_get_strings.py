import unittest

from base_tests import BaseTests


class TestGetStringsIos(BaseTests.BaseGetStringsTest):
    def setUp(self):
        self.data = """
        //      "chinese" = "   欢迎来到我的申请 "   ;
            //"escaped_quote"="MyA\\\"pp";
        "hindi" = "मेरे ऐप का आनंद लें";
        "korean" = "내 앱을 즐기세요";
        """
        self.extension = ".strings"


class TestGetStringsAndroid(BaseTests.BaseGetStringsTest):
    def setUp(self):
        self.data = """
        <?xml version="1.0" encoding="UTF-8"?>
        <resources>
            <!--<string name="chinese">  欢迎来到我的申请  </string>-->
            <!--    <string name="escaped_quote">MyA\\\"pp</string>  -->
            <string name="hindi">मेरे ऐप का आनंद लें</string>
                    <string name="korean">내 앱을 즐기세요</string>
            "3" = "3";
        </resources>
        """
        self.extension = ".xml"


if __name__ == "__main__":
    unittest.main()
