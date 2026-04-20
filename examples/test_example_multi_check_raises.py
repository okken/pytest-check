def test_multi_check_raises(check):
    lst_1 = []
    with check:
        assert lst_1["N/A"] == "Fail 1"
    with check:
        assert lst_1[-1] == "Fail 2"
    lst_2 = ["Success"]
    lst_3 = []
    with check:
        assert lst_2[-1] == "Success"
    with check:
        assert lst_3[-1] == "Success"
