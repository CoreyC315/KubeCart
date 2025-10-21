# Create the User Assigned Identity for AKS
resource "azurerm_user_assigned_identity" "aks_identity" {
  name                = "aks-identity"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# Create the AKS cluster
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "aks-cloudshop-dev"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "cloudshop-k8s"
  kubernetes_version  = "1.32.7"
  sku_tier            = "Free"

  default_node_pool {
    name                 = "systempool"
    vm_size              = "Standard_B2s"
    os_disk_size_gb      = 128
    enable_auto_scaling  = true
    min_count            = 1
    max_count            = 3
    node_count           = 2 # Starting count
    vnet_subnet_id       = azurerm_subnet.aks.id
  }

  identity {
    type         = "UserAssigned"
    #user_assigned_identity_id = azurerm_user_assigned_identity.aks_identity.id
  }

  network_profile {
    network_plugin     = "kubenet"
    load_balancer_sku  = "standard"
    outbound_type      = "loadBalancer"
    service_cidr       = "10.2.0.0/16"
    dns_service_ip     = "10.2.0.10"
    pod_cidr           = "10.244.0.0/16"
  }
}