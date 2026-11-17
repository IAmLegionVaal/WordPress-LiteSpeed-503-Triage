# WordPress / LiteSpeed / Elementor / UpdraftPlus 503 triage

**Status: sustained remediation not verified.** WordPress admin editing and backup activity were associated with lag and HTTP 503. DirectAdmin/LiteSpeed hosting resources were adjusted, but a stable production recovery is not established.

## Actual incident settings (not general recommendations)
| Setting | Observed |
| --- | --- |
| PHP | 8.4 |
| max_execution_time | 600 seconds |
| memory_limit | 512M per PHP process |
| post_max_size | 512M |
| upload_max_filesize | 128M |
| CPU quota | 200% / about 2 cores |
| Account memory quota | ~1.2 GB |

Three 512M-memory-hungry processes may collectively exceed a 1.2 GB account cap. Increasing `memory_limit` and execution time can worsen saturation.

## Evidence-driven workflow
1. Reproduce under approved conditions and correlate HTTP 503 with LiteSpeed/error logs, resource throttling and PHP worker count.
2. Distinguish web SAPI from CLI settings; CLI `php -i` alone does not prove LiteSpeed's effective settings.
3. Monitor CPU, account RAM, IO, database connections, process limits and backup schedule.
4. Stage plugin/backup/cache experiments one variable at a time; verify PHP 8.4 compatibility.
5. Compare baseline and post-change p95 response time, 503 rate, backup duration and Elementor save success.
6. Retain rollback values for quotas and PHP settings.

## Read-only CLI context
```bash
PHP_BIN=php bash scripts/inspect-php-cli-limits.sh
```
Do not publicly expose `phpinfo()`, server error logs, wp-config.php, backup archives or API credentials.

## Acceptance
Elementor and backup finish successfully over a representative period, without new 503s or resource saturation. Not proven in original case.

## Repository scope and operating boundaries

This standalone project separates the historical incident outcome from the
diagnostic tooling. The script collects a narrow set of checks; it does not
automatically perform the manual recovery steps described above. Start with a
nonproduction test and capture a baseline before proposing a configuration
change. Use the least-privileged approved identity and preserve rollback values
in private change records. Stop when required inputs or authorization are missing.

## Evidence and acceptance record

For any new investigation, record the product/runtime versions, UTC observation
time, expected behavior, actual result, exact approved change, rollback owner,
and follow-up observation window in private storage. Publish only a redacted
summary. Mark hypotheses as hypotheses. A successful diagnostic command or green
CI run does not prove the business workflow works. Keep unresolved acceptance
items open until an authorized tester verifies the end-user result.

## Quality, security and licensing

- [Tests and limitations](TESTING.md): syntax, hygiene and isolated regressions.
- [Security guidance](SECURITY.md): safe execution and evidence handling.
- [Source and rights](PROVENANCE.md) and [MIT license](LICENSE).
- [CI runs](https://github.com/IAmLegionVaal/WordPress-LiteSpeed-503-Triage/actions/workflows/validate.yml).
- [Central incident index](https://github.com/IAmLegionVaal/IT-Support-Toolkit-Launcher/blob/main/incident-projects/README.md).
- [Publication and follow-up tracker](https://github.com/IAmLegionVaal/IT-Support-Toolkit-Launcher/issues/1).

Contributions should include synthetic regression coverage and an explicit
statement of what was actually tested. Do not attach raw client evidence to
issues or pull requests. Preserve the historical status unless new evidence
supports a change.
