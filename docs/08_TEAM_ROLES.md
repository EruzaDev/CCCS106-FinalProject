# Team Roles & Contribution Matrix

## Team Information

| Field | Value |
|-------|-------|
| **Project Name** | HonestBallot - Secure Voting Application |
| **Course** | CCCS106 |
| **Semester** | 2nd Semester, AY 2024-2025 |
| **Submission Date** | December 2025 |

---

## Team Members

| Name | Role | Responsibilities |
|------|------|------------------|
| **C-jay B. Lavapie** | Product Lead, Lead Developer, Data & Integration Engineer | Vision & feature prioritization, Flet architecture, storage & emerging tech integration |
| **John Paul Caldo** | UI/UX & Accessibility Designer, QA / Test Coordinator | User interface design, accessibility, testing coordination, bug fixes |
| **Marc Dexter Sael** | Documentation & Release Manager | Technical documentation, user guides, release management |

---

## Role Definitions

### Product Lead / Lead Developer (C-jay B. Lavapie)
- Overall project coordination and vision
- System architecture design (Flet framework)
- Core feature implementation
- Database schema and storage layer
- AI service integration
- Code review and quality assurance

### UI/UX Designer / QA Coordinator (John Paul Caldo)
- Flet UI implementation and components
- User experience design
- Accessibility compliance
- Dashboard layouts (Voter, Politician, COMELEC, NBI)
- Test coordination and bug tracking
- Integration testing

### Documentation & Release Manager (Marc Dexter Sael)
- Project documentation (SRS, technical docs)
- User guide creation
- Release management
- README and setup instructions
- Version control documentation

---

## Contribution Matrix

### Development Contributions

| Component | C-jay | John Paul | Marc Dexter |
|-----------|:-----:|:---------:|:-----------:|
| **Core Voting System** ||||
| User Authentication | ⬤ | ◐ | ○ |
| Vote Casting Logic | ⬤ | ◐ | ○ |
| Election Management | ⬤ | ◐ | ○ |
| Session Management | ⬤ | ○ | ○ |
| **Security Features** ||||
| bcrypt Password Hashing | ⬤ | ○ | ○ |
| Rate Limiting | ⬤ | ○ | ○ |
| Audit Logging | ⬤ | ◐ | ○ |
| Password Policy | ⬤ | ○ | ○ |
| **UI/UX** ||||
| Login/Signup Pages | ◐ | ⬤ | ○ |
| Voter Dashboard | ◐ | ⬤ | ○ |
| Politician Dashboard | ◐ | ⬤ | ○ |
| COMELEC Dashboard | ◐ | ⬤ | ○ |
| NBI Dashboard | ◐ | ⬤ | ○ |
| DatePickerField Component | ○ | ⬤ | ○ |
| Profile Pages | ○ | ⬤ | ○ |
| **Database** ||||
| Schema Design | ⬤ | ○ | ○ |
| User Operations | ⬤ | ○ | ○ |
| Voting Operations | ⬤ | ○ | ○ |
| Legal Records (NBI) | ⬤ | ◐ | ○ |
| **Testing & QA** ||||
| Unit Tests | ◐ | ⬤ | ○ |
| Integration Tests | ◐ | ⬤ | ○ |
| Bug Fixes | ◐ | ⬤ | ○ |
| **Documentation** ||||
| Project Overview | ○ | ○ | ⬤ |
| Technical Docs | ◐ | ○ | ⬤ |
| User Guide | ○ | ◐ | ⬤ |
| README | ◐ | ◐ | ⬤ |

**Legend**: ⬤ = Primary responsibility | ◐ = Contributed | ○ = Not involved

---

### Task Distribution Summary

| Member | Primary Tasks | Secondary Tasks | % Contribution |
|--------|--------------|-----------------|----------------|
| C-jay B. Lavapie | Architecture, Database, Security, Core Features | Code Review, Integration | ~40% |
| John Paul Caldo | UI/UX, Dashboards, Testing, Bug Fixes | Components, QA | ~35% |
| Marc Dexter Sael | Documentation, Release Management | User Guide, README | ~25% |

---

## Development Timeline

| Phase | Duration | Key Deliverables | Lead |
|-------|----------|-----------------|------|
| Planning | Week 1 | Requirements, Architecture | C-jay |
| Database Design | Week 2 | Schema, Setup Scripts | C-jay |
| Core Features | Week 3-4 | Auth, Voting, Sessions | C-jay |
| UI Development | Week 4-5 | All Dashboards, Components | John Paul |
| Security Features | Week 5-6 | bcrypt, Rate Limiting, Audit | C-jay |
| Dashboard Polish | Week 6-7 | NBI, Politician, COMELEC | John Paul |
| Testing | Week 7-8 | Unit, Integration Tests | John Paul |
| Documentation | Week 8-9 | All Docs, User Guide | Marc Dexter |
| Final Review | Week 9 | Bug Fixes, Polish | All |

---

## Communication & Collaboration

### Tools Used
| Tool | Purpose |
|------|---------|
| GitHub | Version control, code review |
| Discord/Messenger | Daily communication |
| Google Meet | Weekly sync meetings |
| VS Code Live Share | Pair programming |
| Trello/Notion | Task tracking |

### Meeting Schedule
- **Weekly Sync**: Saturdays, 2:00 PM
- **Code Review**: Before each merge to main
- **Stand-ups**: Daily async updates in group chat

---

## Git Contribution Summary

> Run `git shortlog -sn` to get actual commit counts

```
Example Output:
    50  C-jay B. Lavapie
    40  John Paul Caldo
    25  Marc Dexter Sael
```

### Branch Strategy
- `main` - Production-ready code
- `feature/*` - Individual feature branches (e.g., feature/date-input)
- `testing-qa` - Test development
- `docs` - Documentation updates

---

*Document Version: 1.0*  
*Last Updated: December 2025*
