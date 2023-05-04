resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "s3_read_policy" {
  name = "s3_read_policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject"
        ]
        Resource = [
          "arn:aws:s3:::rafawainer-aws-glue-tests/input.txt"
        ]
      }
    ]
  })
}

resource "aws_iam_policy" "s3_write_policy" {
  name = "s3_write_policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject"
        ]
        Resource = [
          "arn:aws:s3:::rafawainer-aws-glue-tests/input-processed/*"
        ]
      }
    ]
  })
}

resource "aws_iam_policy" "glue_policy" {
  name = "glue_policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "glue:StartJobRun"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "s3_read_attachment" {
  policy_arn = aws_iam_policy.s3_read_policy.arn
  role = aws_iam_role.lambda_execution_role.name
}

resource "aws_iam_role_policy_attachment" "s3_write_attachment" {
  policy_arn = aws_iam_policy.s3_write_policy.arn
  role = aws_iam_role.lambda_execution_role.name
}

resource "aws_iam_role_policy_attachment" "glue_attachment" {
  policy_arn = aws_iam_policy.glue_policy.arn
  role = aws_iam_role.lambda_execution_role.name
}
