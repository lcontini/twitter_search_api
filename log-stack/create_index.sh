#!/usr/bin/env bash
# From https://github.com/elastic/kibana/issues/3709
set -euo pipefail
url="http://localhost:5601"
index_pattern="filebeat-*"
id="filebeat-*"
time_field="@timestamp"
# Create index pattern
# curl -f to fail on error
curl -f -XPOST -H "Content-Type: application/json" -H "kbn-xsrf: anything" \
  "$url/api/saved_objects/index-pattern/$id" \
  -d"{\"attributes\":{\"title\":\"$index_pattern\",\"timeFieldName\":\"$time_field\"}}"
# Make it the default index
curl -XPOST -H "Content-Type: application/json" -H "kbn-xsrf: anything" \
  "$url/api/kibana/settings/defaultIndex" \
  -d"{\"value\":\"$id\"}"