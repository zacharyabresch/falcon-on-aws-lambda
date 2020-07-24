resource "aws_lambda_function" "this" {
  filename      = pathexpand("../dist/build.zip")
  function_name = "falcon-on-aws-lambda"
  role          = aws_iam_role.this.arn
  handler       = "src.service.handler"
  runtime       = "python3.8"
}
