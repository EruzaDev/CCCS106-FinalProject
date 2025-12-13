# Audit Log Action Types

## Overview
This document describes all the action types used in the HonestBallot audit logging system. Each action type represents a specific category of operation that can be tracked for security and accountability.

## Action Types by Category

### Authentication & Session Management
- **`login`** - User successfully logged in
- **`login_failed`** - Failed login attempt
- **`logout`** - User logged out
- **`account_created`** - New user account created
- **`account_locked`** - Account locked due to too many failed attempts

### Voting Operations
- **`vote_cast`** - Vote successfully cast by a voter
- **`voting_control`** - Voting session started or stopped
- **`vote_result`** - Election results accessed or exported

### Legal Records (NBI)
- **`legal_record`** - New legal record added for a politician
- **`legal_record_edit`** - Existing legal record updated (title, description, date, type)
- **`legal_record_status`** - Legal record status changed (pending, verified, dismissed, rejected)

### Achievement Verification (COMELEC)
- **`verification`** - Achievement verification status changed
- **`verification_request`** - New achievement verification requested

### User Management
- **`user_created`** - New user created by administrator
- **`user_updated`** - User information updated
- **`user_deleted`** - User account deleted
- **`role_changed`** - User role modified

### Content Management
- **`news_post`** - News or announcement posted
- **`profile_updated`** - User profile information updated

## Role-Based Access to Audit Logs

### COMELEC Officials
Can view **all** audit logs across the system.

### NBI Officers
Can view logs for:
- `legal_record` - Legal records they manage
- `legal_record_edit` - Record modifications
- `legal_record_status` - Status changes
- `login` - Authentication events
- `logout` - Sign-out events

### Politicians
Can view logs for:
- `verification` - Achievement verifications related to them
- `legal_record` - Legal records about them
- `legal_record_edit` - Changes to their legal records
- `legal_record_status` - Status updates on their records
- `vote_result` - Election results

### Voters
Limited access - typically only see public information, no direct audit log access.

## Audit Log Fields

Each audit log entry contains:
- **id** - Unique identifier
- **action** - Human-readable description
- **action_type** - Category code (see above)
- **description** - Detailed information
- **user_id** - ID of user who performed the action
- **user_role** - Role of the user (comelec, nbi, politician, voter)
- **target_type** - Type of resource affected (politician, legal_record, vote, etc.)
- **target_id** - ID of the affected resource
- **details** - JSON with additional context (optional)
- **ip_address** - Source IP address (optional)
- **created_at** - Timestamp of the action

## Usage Examples

### Adding a Legal Record
```python
db.log_action(
    action="Legal Record Added",
    action_type="legal_record",
    description="Added record: Graft and Corruption Case",
    user_id=nbi_officer_id,
    user_role="nbi",
    target_type="politician",
    target_id=politician_id,
)
```

### Updating a Legal Record
```python
db.log_action(
    action="Legal Record Updated",
    action_type="legal_record_edit",
    description="Updated record: Tax Case Investigation (status changed to verified)",
    user_id=nbi_officer_id,
    user_role="nbi",
    target_type="legal_record",
    target_id=record_id,
)
```

### Verifying a Legal Record
```python
db.log_action(
    action="Legal Record Verified",
    action_type="legal_record_status",
    description="Verified record: Criminal Case Filing",
    user_id=nbi_officer_id,
    user_role="nbi",
    target_type="legal_record",
    target_id=record_id,
)
```

## Best Practices

1. **Always log sensitive operations** - Especially those involving data modification or access to sensitive information
2. **Use descriptive action descriptions** - Include key details like record titles or affected entities
3. **Include target information** - Specify both target_type and target_id for traceability
4. **Log both success and failure** - Track failed attempts for security monitoring
5. **Maintain consistency** - Use the standardized action types defined in this document

## Security Considerations

- Audit logs are **append-only** - they cannot be modified or deleted by users
- Access to audit logs is **role-based** and strictly controlled
- Logs capture **who did what, when, and to what** for full accountability
- Failed login attempts are tracked to prevent **credential stuffing attacks**
- All COMELEC actions are logged for **election integrity and transparency**

## Related Documentation
- See `SECURITY_ENGINEERING.md` for security threat analysis
- See `04_DATA_MODEL.md` for database schema details
- See `02_FEATURE_LIST.md` for feature overview
