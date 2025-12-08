# Security Engineering Report - HonestBallot

## Executive Summary

HonestBallot is a secure electronic voting application built with the Flet framework (Python). This document outlines the security architecture, threat model, and defensive measures implemented to protect the integrity of the voting process and user data.

---

## 1. Threat Model (STRIDE Analysis)

### 1.1 STRIDE Threat Matrix

| Threat Category | Threat Description | Asset at Risk | Mitigation Implemented |
|----------------|-------------------|---------------|----------------------|
| **S**poofing | Attacker impersonates legitimate voter | User accounts | bcrypt password hashing, session tokens, login throttling |
| **T**ampering | Modification of votes or election results | Vote integrity | Database constraints, audit logging, COMELEC-only controls |
| **R**epudiation | User denies casting a vote | Vote records | Comprehensive audit logs with timestamps, user IDs |
| **I**nformation Disclosure | Exposure of voter choices or credentials | User privacy | Password hashing, no plaintext storage, role-based access |
| **D**enial of Service | Brute-force login attempts | System availability | Account lockout after 5 failed attempts, 15-min cooldown |
| **E**levation of Privilege | Voter gains admin access | System integrity | Role-based access control (RBAC), server-side authorization |

### 1.2 Key Threats & Mitigations Detail

#### Threat 1: Credential Stuffing / Brute Force Attacks
- **Risk Level:** HIGH
- **Attack Vector:** Automated login attempts with leaked credentials
- **Mitigation:**
  ```python
  # app/storage/database.py
  MAX_LOGIN_ATTEMPTS = 5
  LOCKOUT_DURATION_MINUTES = 15
  
  def is_account_locked(self, identifier):
      failed_attempts = self.get_failed_attempts_count(identifier, self.LOCKOUT_DURATION_MINUTES)
      return failed_attempts >= self.MAX_LOGIN_ATTEMPTS
  ```

#### Threat 2: Password Database Compromise
- **Risk Level:** CRITICAL
- **Attack Vector:** SQL injection or database file theft
- **Mitigation:** bcrypt hashing with cost factor 12 (see Section 3)

#### Threat 3: Session Hijacking
- **Risk Level:** MEDIUM
- **Attack Vector:** Token theft or prediction
- **Mitigation:** Cryptographically secure tokens, 30-minute timeout (see Section 4)

#### Threat 4: Privilege Escalation
- **Risk Level:** HIGH
- **Attack Vector:** Manipulating role assignments
- **Mitigation:** Server-side role enforcement, audit logging of privilege changes

---

## 2. Input Validation & Sanitization Strategy

### 2.1 Validation Layers

**Layer 1: UI Validation (Flet TextField constraints)**
- max_length limits
- input_filter for allowed characters
- Required field enforcement

**Layer 2: Application Validation (Python)**
- Type checking
- Format validation (email regex, password policy)
- Business logic rules

**Layer 3: Database Constraints**
- Parameterized queries (SQL injection prevention)
- UNIQUE constraints
- FOREIGN KEY integrity

### 2.2 SQL Injection Prevention

All database queries use **parameterized statements**:

```python
# SECURE - Parameterized query
self.cursor.execute('''
    SELECT id, username, email, role, password_hash FROM users
    WHERE email = ?
''', (email,))

# NEVER - String concatenation (vulnerable)
# query = f"SELECT * FROM users WHERE email = '{email}'"  # DON'T DO THIS
```

### 2.3 Password Validation

```python
# app/password_policy.py
class PasswordPolicy:
    MIN_LENGTH = 8
    MAX_LENGTH = 128
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_DIGIT = True
    REQUIRE_SPECIAL = True
    
    @classmethod
    def validate(cls, password, username=None, email=None):
        errors = []
        
        if len(password) < cls.MIN_LENGTH:
            errors.append(f"Password must be at least {cls.MIN_LENGTH} characters")
        
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        # ... additional checks
        
        # Prevent password containing username
        if username and username.lower() in password.lower():
            errors.append("Password cannot contain your username")
        
        return len(errors) == 0, errors
```

### 2.4 Email Validation

```python
import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

---

## 3. Password Hashing Algorithm & Parameters

### 3.1 Algorithm Selection: bcrypt

| Algorithm | Status | Why/Why Not |
|-----------|--------|-------------|
| MD5 | ❌ Rejected | Cryptographically broken, fast to crack |
| SHA-256 | ❌ Rejected | Too fast, vulnerable to GPU attacks |
| **bcrypt** | ✅ Selected | Adaptive cost, designed for passwords |
| Argon2 | ⚠️ Alternative | Newer, but bcrypt well-tested |

### 3.2 bcrypt Implementation

```python
# app/storage/database.py
import bcrypt

def hash_password(self, password):
    """Hash password using bcrypt (secure, salted hashing)"""
    if isinstance(password, str):
        password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

def verify_password(self, password, password_hash):
    """Verify password against bcrypt hash"""
    if isinstance(password, str):
        password = password.encode('utf-8')
    if isinstance(password_hash, str):
        password_hash = password_hash.encode('utf-8')
    try:
        return bcrypt.checkpw(password, password_hash)
    except Exception:
        return False
```

### 3.3 Cost Factor Justification

| Cost Factor | Hash Time (approx) | Security Level | Our Choice |
|-------------|-------------------|----------------|------------|
| 10 | ~100ms | Minimum acceptable | |
| **12** | ~300ms | **Recommended** | ✅ |
| 14 | ~1.2s | High security | |

**Rationale for Cost Factor 12:**
- **Security:** 2^12 = 4,096 iterations, providing strong brute-force resistance
- **Performance:** ~300ms hash time is imperceptible to users during login
- **Future-proof:** Can increase to 13-14 as hardware improves
- **Industry Standard:** OWASP recommends minimum cost factor 10, with 12+ preferred

### 3.4 Salt Management

bcrypt automatically generates and embeds a **128-bit random salt** in each hash:

```
$2b$12$cXGfMmzWc.jgBP7oiil/lus0Zbqc77qjGhAjRuRR7WXMp5TdR4jDy
 │  │  │                      │
 │  │  │                      └── Hash (31 chars)
 │  │  └── Salt (22 chars, Base64)
 │  └── Cost factor (12)
 └── Algorithm identifier (2b = bcrypt)
```

---

## 4. Session Management Controls

### 4.1 Session Architecture

```python
# app/state/session_manager.py
class SessionManager:
    SESSION_TIMEOUT = timedelta(minutes=30)  # Configurable via .env
    
    def __init__(self, db=None):
        self.sessions = {}  # In-memory session store
        self.db = db or Database()
    
    def create_session(self, user_id, username, email, role):
        """Create a new session with cryptographically secure token"""
        token = secrets.token_urlsafe(32)  # 256-bit random token
        
        self.sessions[token] = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "role": role,
            "created_at": datetime.now(),
            "last_activity": datetime.now(),
        }
        
        return token
```

### 4.2 Session Security Controls

| Control | Implementation | Purpose |
|---------|---------------|---------|
| **Token Generation** | `secrets.token_urlsafe(32)` | 256-bit cryptographically random |
| **Session Timeout** | 30 minutes inactivity | Limit exposure window |
| **Activity Tracking** | `last_activity` timestamp | Detect idle sessions |
| **Server-side Storage** | In-memory dictionary | Tokens cannot be forged |
| **Session Invalidation** | `end_session()` on logout | Clean termination |

### 4.3 Session Timeout Implementation

```python
def verify_session(self, token):
    """Verify session is valid and not expired"""
    if token not in self.sessions:
        return None
    
    session = self.sessions[token]
    
    # Check for timeout
    if datetime.now() - session["last_activity"] > self.SESSION_TIMEOUT:
        self.end_session(token)  # Auto-cleanup expired sessions
        return None
    
    # Update last activity (session renewal)
    session["last_activity"] = datetime.now()
    return session
```

### 4.4 Desktop App Considerations

Since HonestBallot is a **Flet desktop application** (not web-based):

| Web Security | Desktop Equivalent |
|--------------|-------------------|
| HTTP-only cookies | Not applicable (no browser) |
| CSRF tokens | Not applicable (no cross-site requests) |
| Secure flag | Not applicable (no HTTPS in local app) |
| SameSite | Not applicable |

**Desktop-specific protections:**
- Session tokens stored only in application memory
- No persistent token storage (cleared on app close)
- Single-user context per application instance

---

## 5. Logging & Monitoring Scope

### 5.1 Security Events Logged

```python
# app/security_logger.py
class AuthLogger:
    @staticmethod
    def login_success(username, user_id, role, ip_address=None):
        logger.info(f"LOGIN_SUCCESS | user={username} | user_id={user_id} | role={role}")
    
    @staticmethod
    def login_failed(username, reason="Invalid credentials", attempts_remaining=None):
        logger.warning(f"LOGIN_FAILED | user={username} | reason={reason}")
    
    @staticmethod
    def account_locked(username, duration_minutes):
        logger.warning(f"ACCOUNT_LOCKED | user={username} | duration={duration_minutes}m")
    
    @staticmethod
    def logout(username, user_id, reason="user_initiated"):
        logger.info(f"LOGOUT | user={username} | user_id={user_id}")
    
    @staticmethod
    def privilege_escalation(username, old_role, new_role, changed_by):
        logger.warning(f"PRIVILEGE_CHANGE | user={username} | {old_role} -> {new_role}")
```

### 5.2 Audit Log Categories

| Category | Events Logged | Retention |
|----------|--------------|-----------|
| **Authentication** | Login success/failure, logout, lockout | Permanent |
| **Authorization** | Role changes, permission denials | Permanent |
| **Voting** | Vote cast, vote changes (if allowed) | Permanent |
| **Administration** | User creation, status changes | Permanent |
| **Legal Records** | NBI record additions, verifications | Permanent |

### 5.3 Log Format

```
2025-12-07 14:32:15 | INFO     | honestballot | LOGIN_SUCCESS | user=admin | user_id=5 | role=comelec
2025-12-07 14:35:22 | WARNING  | honestballot | LOGIN_FAILED | user=unknown | reason=Invalid credentials | attempts_remaining=4
2025-12-07 14:40:00 | WARNING  | honestballot | ACCOUNT_LOCKED | user=attacker | duration=15m
```

### 5.4 Database Audit Trail

```python
# app/storage/database.py
def log_action(self, action, action_type, description=None, user_id=None, 
               user_role=None, target_type=None, target_id=None, details=None):
    """Log an action to the audit log"""
    self.cursor.execute('''
        INSERT INTO audit_logs 
        (action, action_type, description, user_id, user_role, target_type, target_id, details)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (action, action_type, description, user_id, user_role, target_type, target_id, 
          json.dumps(details) if details else None))
    self.connection.commit()
```

---

## 6. Error Handling (No Sensitive Leakage)

### 6.1 Principles

1. **Generic Error Messages** - Never reveal internal details to users
2. **Detailed Internal Logging** - Full context for debugging
3. **Graceful Degradation** - App remains functional after errors

### 6.2 Implementation Examples

```python
# SECURE - Generic user message, detailed internal log
def handle_login(self, username, password):
    try:
        user = self.db.verify_user(username, password)
        if not user:
            # Log specific reason internally
            auth_logger.login_failed(username, "Invalid credentials")
            # Show generic message to user
            self.show_error_dialog("Login Failed", "Invalid email or password.")
    except Exception as e:
        # Log full exception internally
        logger.error(f"Login error: {e}", exc_info=True)
        # Show generic message to user
        self.show_error_dialog("Error", "An error occurred. Please try again.")

# INSECURE - Don't do this!
# self.show_error_dialog("Error", f"Database error: {str(e)}")  # Leaks DB info
# self.show_error_dialog("Error", "User not found in database")  # Reveals user enumeration
```

### 6.3 Error Message Guidelines

| Scenario | ❌ Insecure Message | ✅ Secure Message |
|----------|-------------------|------------------|
| Wrong password | "Password incorrect" | "Invalid email or password" |
| User not found | "User does not exist" | "Invalid email or password" |
| Account locked | "Locked due to SQLite constraint" | "Too many attempts. Try again later." |
| Database error | "sqlite3.OperationalError: ..." | "An error occurred. Please try again." |

---

## 7. OWASP Top 10 Defense Matrix

### 7.1 Relevant Vulnerabilities & Mitigations

| OWASP Category | Relevance | Mitigation Status |
|----------------|-----------|-------------------|
| **A01: Broken Access Control** | HIGH | ✅ RBAC, server-side authorization |
| **A02: Cryptographic Failures** | HIGH | ✅ bcrypt, no plaintext passwords |
| **A03: Injection** | HIGH | ✅ Parameterized SQL queries |
| **A04: Insecure Design** | MEDIUM | ✅ Threat modeling, defense in depth |
| **A05: Security Misconfiguration** | MEDIUM | ✅ .env for secrets, secure defaults |
| **A06: Vulnerable Components** | LOW | ⚠️ Regular dependency updates needed |
| **A07: Auth Failures** | HIGH | ✅ bcrypt, lockout, session mgmt |
| **A08: Data Integrity Failures** | MEDIUM | ✅ Audit logging, DB constraints |
| **A09: Logging Failures** | MEDIUM | ✅ Comprehensive security logging |
| **A10: SSRF** | LOW | N/A (no outbound requests) |

### 7.2 Detailed Mitigations

#### A01: Broken Access Control
```python
# Role-based access control in UI and backend
def show_comelec_dashboard(self):
    if self.current_session["role"] != "comelec":
        self.show_error_dialog("Access Denied", "COMELEC access required")
        return
    # ... proceed with dashboard

# Database-level role filtering
def get_audit_logs_for_role(self, viewer_role):
    role_permissions = {
        'comelec': ['all'],
        'nbi': ['legal_record', 'login', 'logout'],
        'politician': ['verification', 'legal_record'],
    }
    # Filter logs based on role permissions
```

#### A02: Cryptographic Failures
- ✅ bcrypt for password hashing (cost factor 12)
- ✅ No plaintext password storage
- ✅ Secure random token generation (`secrets.token_urlsafe`)
- ✅ Passwords never logged or displayed

#### A03: Injection
```python
# All queries use parameterized statements
self.cursor.execute(
    'SELECT * FROM users WHERE email = ?',  # Parameterized
    (email,)  # Value passed separately
)
```

#### A07: Identification and Authentication Failures
- ✅ Strong password policy (8+ chars, complexity requirements)
- ✅ Account lockout after 5 failed attempts
- ✅ 15-minute lockout duration
- ✅ 30-minute session timeout
- ✅ Secure session token generation

---

## 8. Security Configuration

### 8.1 Environment Variables (.env)

```bash
# .env.example - Copy to .env and configure

# Security Settings
SECRET_KEY=change-this-in-production-to-a-secure-random-key
SESSION_TIMEOUT_MINUTES=30
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION_MINUTES=15

# Password Hashing
BCRYPT_ROUNDS=12

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log
```

### 8.2 Secure Defaults

```python
# app/config.py
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
    SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))
    MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
    LOCKOUT_DURATION_MINUTES = int(os.getenv("LOCKOUT_DURATION_MINUTES", "15"))
    
    @classmethod
    def validate(cls):
        warnings = []
        if cls.SECRET_KEY == "change-this-in-production":
            warnings.append("WARNING: Using default SECRET_KEY!")
        return warnings
```

---

## 9. Testing Coverage

### 9.1 Security Test Summary

| Test Category | Tests | Status |
|---------------|-------|--------|
| Password Hashing | 4 | ✅ Pass |
| Password Policy | 18 | ✅ Pass |
| Credential Stuffing Protection | 7 | ✅ Pass |
| Session Management | 16 | ✅ Pass |
| Audit Logging | 8 | ✅ Pass |
| **Total Security Tests** | **53** | ✅ Pass |

### 9.2 Manual Security Test Matrix

| Test Case | Steps | Expected Result | Status |
|-----------|-------|-----------------|--------|
| Brute Force Protection | Attempt 6 failed logins | Account locked, 15-min message | ✅ |
| Session Timeout | Wait 30+ minutes idle | Auto-logout on next action | ✅ |
| Role Enforcement | Voter access COMELEC page | Access denied | ✅ |
| SQL Injection | Enter `' OR 1=1--` as email | Login failed (no bypass) | ✅ |
| Password Policy | Enter "weak" as password | Rejected with error list | ✅ |

---

## 10. Recommendations for Production

1. **Generate Strong SECRET_KEY:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **Increase bcrypt Cost Factor** to 13-14 if hardware allows

3. **Enable File-based Logging** in production:
   ```bash
   LOG_LEVEL=WARNING
   LOG_FILE=/var/log/honestballot/app.log
   ```

4. **Regular Dependency Updates:**
   ```bash
   pip install --upgrade bcrypt flet
   ```

5. **Database Backups:** Implement scheduled SQLite backups

---

## Appendix A: Security Checklist

- [x] Passwords hashed with bcrypt (cost 12)
- [x] No plaintext password storage
- [x] Parameterized SQL queries throughout
- [x] Account lockout after failed attempts
- [x] Session timeout implemented
- [x] Secure session token generation
- [x] Role-based access control
- [x] Comprehensive audit logging
- [x] Generic error messages (no info leakage)
- [x] Password complexity policy
- [x] Configuration via environment variables
- [x] Security-focused unit tests

---

*Document Version: 1.0*
*Last Updated: December 7, 2025*
*Author: HonestBallot Development Team*
