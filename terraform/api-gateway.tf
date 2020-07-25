resource "aws_api_gateway_rest_api" "this" {
  name        = "falcon-on-aws"
  description = "The API Gateway connecting the Falcon Lambda"
}

resource "aws_api_gateway_resource" "degs" {
  rest_api_id = aws_lambda_function.this.id
  parent_id   = aws_api_gateway_rest_api.this.root_resource_id
  path_part   = "degs"
}

resource "aws_api_gateway_method" "degs" {
  rest_api_id   = aws_lambda_function.this.id
  resource_id   = aws_api_gateway_rest_api.this.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "this" {
  rest_api_id = aws_lambda_function.this.id
  resource_id = aws_api_gateway_method.degs.resource_id
  http_method = aws_api_gateway_method.degs.http_method

  integration_http_method = "GET"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.this.invoke_arn
}

resource "aws_api_gateway_deployment" "this" {
  depends_on = [
    aws_api_gateway_integration.this
  ]

  rest_api_id = aws_api_gateway_rest_api.this.id
  stage_name  = "default"
}

