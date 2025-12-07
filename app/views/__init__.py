# Views / Page Components
from .login_page import LoginPage
from .signup_page import SignupPage
from .home_page import HomePage
from .settings_page import SettingsPage
from .profile_page import ProfilePage
from .comelec_dashboard import ComelecDashboard
from .user_management import UserManagement
from .election_results import ElectionResults
from .voter_dashboard import VoterDashboard
from .politician_profile import PoliticianProfile
from .candidate_comparison import CandidateComparison
from .voting_page import VotingPage
from .politician_dashboard import PoliticianDashboard
from .nbi_dashboard import NBIDashboard
from .audit_log_page import AuditLogPage
from .analytics_page import AnalyticsPage

__all__ = [
    'LoginPage',
    'SignupPage', 
    'HomePage',
    'SettingsPage',
    'ProfilePage',
    'ComelecDashboard',
    'UserManagement',
    'ElectionResults',
    'VoterDashboard',
    'PoliticianProfile',
    'CandidateComparison',
    'VotingPage',
    'PoliticianDashboard',
    'NBIDashboard',
    'AuditLogPage',
    'AnalyticsPage',
]
