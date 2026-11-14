#!/usr/bin/env bash
set -euo pipefail
cd /workspace/Ikke-trening
find plugin tests -type d -exec chmod 755 {} +
find plugin tests -type f -exec chmod 644 {} +
docker compose up -d wordpress
for attempt in {1..40}; do
  if curl --silent --fail http://localhost:8080/wp-login.php > /dev/null; then break; fi
  if [[ "$attempt" = 40 ]]; then exit 1; fi
  sleep 1
done
if ! docker compose run --rm cli wp core is-installed; then
  docker compose run --rm cli wp core install --url=http://localhost:8080 --title='GymNotFound local test' --admin_user=gnf_test_admin --admin_password=LocalTestOnly_2026 --admin_email=local-test@example.invalid --skip-email
fi
docker compose run --rm cli wp plugin activate gymnotfound
gnf_page_id=$(docker compose run --rm cli wp option get gnf_page_id 2>/dev/null || true)
if [[ ! "$gnf_page_id" =~ ^[1-9][0-9]*$ ]]; then
  gnf_page_id=$(docker compose run --rm cli wp post create --post_type=page --post_title=GymNotFound --post_content='[gymnotfound_app]' --post_status=publish --porcelain)
  docker compose run --rm cli wp option update gnf_page_id "$gnf_page_id"
fi
curl --silent --fail "http://localhost:8080/?page_id=$gnf_page_id" > /tmp/gnf-page-check.html
rg --quiet 'id="gymnotfound"' /tmp/gnf-page-check.html
GNF_APP_PATH="/?page_id=$gnf_page_id" node scripts/smoke.cjs
printf 'PASS GymNotFound local WordPress runtime; app page %s\n' "$gnf_page_id"
