# Risk / Constraint Notes & Future Enhancements

## Project Constraints

### Technical Constraints

| Constraint | Impact | Mitigation |
|-----------|--------|------------|
| **SQLite Database** | Limited concurrent access, not suitable for high-traffic | Acceptable for POC; migrate to PostgreSQL for production |
| **Desktop-Only** | No mobile/web access | Flet supports web deployment for future phases |
| **Single Machine** | No distributed deployment | Containerization possible for scaling |
| **Python Runtime** | Requires Python installation | Can bundle as executable using PyInstaller |
| **No External APIs** | All data self-contained | Keeps system isolated but limits real-time data |

### Resource Constraints

| Constraint | Impact | Mitigation |
|-----------|--------|------------|
| **Development Time** | Limited feature scope | Focus on core voting and AI features |
| **Team Size** | 3-4 members | Clear role division, parallel development |
| **Budget** | No paid services | Use only free/open-source tools |
| **Testing Resources** | No dedicated QA team | Developers write their own tests |

### Scope Constraints

| Constraint | Impact | Mitigation |
|-----------|--------|------------|
| **Educational Purpose** | Not for real elections | Clear disclaimer in documentation |
| **Proof of Concept** | Not production-ready | Focus on demonstrating capabilities |
| **No Real NBI Integration** | Mock legal records | Simulated NBI workflow |
| **No COMELEC Integration** | Standalone system | Independent election management |

---

## Risk Assessment

### High Priority Risks

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| **Data Loss** | Medium | High | Regular backups, transaction logging |
| **Session Hijacking** | Low | High | Token-based auth, session timeout |
| **SQL Injection** | Low | High | Parameterized queries throughout |
| **Duplicate Voting** | Low | Critical | Database constraints, validation checks |

### Medium Priority Risks

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| **AI Bias** | Medium | Medium | Neutral keyword dictionaries, testing |
| **Poor UX** | Medium | Medium | User testing, iterative design |
| **Performance Issues** | Low | Medium | Efficient queries, indexing |
| **Dependency Updates** | Medium | Low | Pin versions in requirements.txt |

### Low Priority Risks

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| **Cross-Platform Issues** | Low | Low | Testing on Windows, macOS, Linux |
| **Documentation Gaps** | Medium | Low | Comprehensive docs folder |
| **Code Maintainability** | Low | Medium | Clean architecture, comments |

---

## Known Limitations

### Current System Limitations

1. **No Real-Time Updates**
   - Vote counts don't auto-refresh
   - Workaround: Manual refresh button

2. **Single Language**
   - English only interface and AI
   - Filipino support planned for Phase 2

3. **No Encryption at Rest**
   - Database file is unencrypted
   - Passwords are hashed, but other data is plain text

4. **Limited Scalability**
   - SQLite handles ~100 concurrent users
   - Not suitable for nationwide elections

5. **Basic AI**
   - Rule-based, not learning
   - Limited vocabulary coverage

6. **No Accessibility Features**
   - No screen reader support
   - No high contrast mode

---

## Future Enhancements

### Phase 2 Enhancements (Near-term)

| Feature | Priority | Effort | Description |
|---------|----------|--------|-------------|
| Filipino Language Support | High | Medium | Add Filipino keyword dictionaries |
| Web Deployment | High | Medium | Deploy as web app using Flet web |
| Email Notifications | Medium | Low | Send vote confirmations |
| Dark Mode | Medium | Low | Alternative color scheme |
| Data Export | Medium | Low | Export results to CSV/PDF |
| Profile Images | Low | Low | Upload custom profile pictures |

### Phase 3 Enhancements (Medium-term)

| Feature | Priority | Effort | Description |
|---------|----------|--------|-------------|
| PostgreSQL Migration | High | Medium | Production-ready database |
| Machine Learning AI | Medium | High | Train on voter feedback |
| Mobile App | Medium | High | Native iOS/Android apps |
| Multi-Election Support | Medium | Medium | Multiple concurrent elections |
| Real-Time Dashboard | Medium | Medium | WebSocket-based live updates |
| Two-Factor Authentication | High | Medium | SMS/Email verification |

### Phase 4 Enhancements (Long-term)

| Feature | Priority | Effort | Description |
|---------|----------|--------|-------------|
| Blockchain Audit Trail | Medium | High | Immutable vote records |
| Biometric Authentication | Low | High | Fingerprint/Face ID |
| API for Third Parties | Medium | Medium | Public election data API |
| Advanced Analytics | Medium | High | Predictive voting patterns |
| Multi-Language NLP | Low | High | Support for multiple languages |
| Accessibility Compliance | High | Medium | WCAG 2.1 compliance |

---

## Technical Debt

| Item | Impact | Priority to Fix |
|------|--------|-----------------|
| Some hardcoded strings | Localization difficulty | Medium |
| Limited error handling in UI | Poor user experience | High |
| No database migrations | Schema updates are manual | Medium |
| Inconsistent naming conventions | Code readability | Low |
| Missing type hints | IDE support, documentation | Low |

---

## Lessons Learned

### What Worked Well
1. **Flet Framework** - Rapid UI development with Python
2. **SQLite for POC** - Zero configuration, file-based
3. **Rule-Based AI** - Transparent, explainable decisions
4. **Modular Architecture** - Easy to extend and test

### What Could Be Improved
1. **Earlier Testing** - Should have written tests from start
2. **UI Design First** - Wireframes before coding
3. **Documentation Cadence** - Document as you build
4. **Code Reviews** - More frequent peer reviews

---

## Recommendations for Similar Projects

1. **Start with Requirements** - Clear scope prevents feature creep
2. **Choose Right Database** - SQLite for POC, PostgreSQL for production
3. **Test Early and Often** - Don't leave testing to the end
4. **Version Control** - Use Git branches effectively
5. **Document Decisions** - Future you will thank present you
6. **Keep It Simple** - MVP first, enhancements later

---

*Document Version: 1.0*  
*Last Updated: December 2025*
