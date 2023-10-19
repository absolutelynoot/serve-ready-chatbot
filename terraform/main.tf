# Sage Maker
resource "aws_sagemaker_app" "servebot_llm" {
  domain_id         = aws_sagemaker_domain.servebot_llm.id
  user_profile_name = aws_sagemaker_user_profile.servebot_llm.user_profile_name
  app_name          = "servebot_llm"
  app_type          = "JupyterServer"
}