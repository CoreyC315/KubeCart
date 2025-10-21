# Configure the Azure Provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Define the main resource group
resource "azurerm_resource_group" "rg" {
  name     = "rg-cloudshop-dev"
  location = "eastus"
}