from shippocon import license_text_generator


def test_get_license_text():
    license_text_generator.B64_LICENSE_TEXT = "44GX44Gj44G944Kz44Oz"
    assert license_text_generator.get_license_text() == "しっぽコン"
