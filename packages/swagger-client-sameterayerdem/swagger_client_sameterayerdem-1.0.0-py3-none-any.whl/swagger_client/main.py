import swagger_client
from swagger_client import Configuration, ApiClient, AuthApi, ShopsApi, SupplierApi

# configuration

configuration = Configuration()
configuration.username="orucmarket"
configuration.password="Oruc123*"
configuration.host="https://locals-integration-api-gateway.artisan.getirapi.com"
api_client = ApiClient(configuration=configuration)
api_instance = AuthApi(api_client=api_client)
sup = SupplierApi(api_client=api_client)
ShopsApi(api_client=api_client)

# get token

token = api_instance.login()
api_client.default_headers["Authorization"] = "Bearer " + token.data.token
supplier = sup.get_supplier()

#print(supplier)
chainList=supplier.data.chains
chainlist=[]
for chain in chainList:
    chainlist.append(chain.id)

print(chainlist)

api_client.default_headers["Authorization"] = "Bearer " + "sa"

supplier = sup.get_supplier()
