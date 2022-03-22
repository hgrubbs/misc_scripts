# Terraform plan scanner

This utility walks through a Terraform directory structure and init/plans all chunks within. Chunks that do not plan clean are reported to Slack, with plan result added as a threaded reply to messages indicating a chunk failed to plan clean.

Individual chunks that you do not want scanned are skipped if the file `.skip_plan_scanner` exists.

The following ENV variables must be set for the utility to post to Slack. If you don't want Slack posts, don't set them.

- `SLACK_CHANNEL_ID` : channel ID which resolves to a Slack channel
- `SLACK_OAUTH_TOKEN` : OAuth token to authenticate with Slack API
