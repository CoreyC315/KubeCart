# Create the Azure Container Registry
resource "azurerm_container_registry" "acr" {
  name                = "cloudshopacr12345"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = true
}