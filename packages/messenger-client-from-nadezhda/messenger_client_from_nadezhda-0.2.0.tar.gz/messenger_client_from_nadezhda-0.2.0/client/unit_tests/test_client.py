# """ Тестирование клиента. """
# from unittest import TestCase
# import unitest as unitest
# from client import create_presence, process_ans
# from common.variables import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, \
#     RESPONSE, ERROR
#
#
# class TestClient(TestCase):
#     def setUp(self):
#         pass
#
#     # Тест корректного запроса, тест приветствия(все данные в наличии)
#     def test_def_presence(self):
#         test = create_presence()
#         # время необходимо приравнять принудительно, иначе тест никогда не
#         # будет пройден????
#         test[TIME] = 1.1
#         self.assertEqual(
#             test, {
#                 ACTION: PRESENCE, TIME: 1.1, USER: {
#                     ACCOUNT_NAME: 'Guest'}})
#
#     # Тест корректного разбора 200
#     def test_200_ans(self):
#         self.assertEqual(process_ans(
#             {RESPONSE: 400, ERROR: 'Bad Request'}), '400: Bad Request')
#
#     # Тест корректного разбора 400
#     def test_400_ans(self):
#         self.assertEqual(process_ans(
#             {RESPONSE: 400, ERROR: 'Bad Request'}), '400: Bad Request')
#
#     # Тест исключения без поля RESPONSE
#     def test_no_response(self):
#         self.assertEqual(ValueError, process_ans, {ERROR: 'Bad Request'})
#
#     def tearDown(self):
#         pass
#
#
# if __name__ == '__main__':
#     unitest.main()
#
# # из терминала: python3 -m unitest test_client
