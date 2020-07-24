terraform {
  backend "remote" {
    organization = "pen-and-paper-programmer"
    workspaces {
      name = "falcon-on-aws-lambda"
    }
  }
}
