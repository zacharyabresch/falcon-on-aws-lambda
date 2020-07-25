data "archive_file" "dummy" {
  type        = "zip"
  output_path = "${path.module}/build.zip"

  source {
    content  = "hello dummy"
    filename = "dummy.txt"
  }
}

resource "aws_lambda_function" "this" {
  filename      = data.archive_file.dummy.output_path
  function_name = "falcon-on-aws-lambda"
  role          = aws_iam_role.this.arn
  handler       = "src.service.handler"
  runtime       = "python3.8"
}
