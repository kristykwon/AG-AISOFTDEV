import React from 'react';

// ================================================================================================
// 1. ICON COMPONENTS
// ================================================================================================
// Note: In a real-world application, these would likely be in a dedicated `components/icons` directory.

/**
 * The main application logo icon.
 */
const LogoWIcon = () => (
  <div className="bg-white w-8 h-8 rounded-md flex items-center justify-center">
    <svg width="20" height="14" viewBox="0 0 20 14" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M2.144 0.463998L0 13.252L6.016 13.204L7.096 7.492L9.88 13.156L12.928 2.236L14.936 13.156L20 13.06L17.856 0.315998L13.96 0.363998L11.512 9.556L8.872 0.411998L2.144 0.463998Z" fill="#1E293B"/>
    </svg>
  </div>
);

/**
 * A notification bell icon.
 */
const BellIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-300 hover:text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
  </svg>
);

/**
 * A checkmark icon for completed tasks.
 */
const CompletedCheckIcon = () => (
  <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="12" fill="#2DD4BF"/>
    <path d="M17.2738 8.52628L10.3798 15.4203L7.22754 12.268" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

/**
 * An empty check circle for incomplete tasks.
 */
const IncompleteCheckIcon = () => (
  <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="11.5" fill="white" stroke="#E5E7EB"/>
    <path d="M17.2738 8.52628L10.3798 15.4203L7.22754 12.268" stroke="#D1D5DB" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// ================================================================================================
// 2. ATOMIC & REUSABLE UI COMPONENTS
// ================================================================================================

/**
 * A generic card component with a title and content area.
 * @param {string} title - The title of the card.
 * @param {React.ReactNode} children - The content to be rendered inside the card.
 * @param {string} [className] - Optional additional CSS classes.
 */
const Card = ({ title, children, className = '' }) => (
  <div className={`bg-white rounded-2xl shadow-lg p-6 flex flex-col ${className}`}>
    <h2 className="text-xl font-bold text-slate-800 mb-4">{title}</h2>
    <div className="flex-grow">
      {children}
    </div>
  </div>
);

/**
 * A reusable button component.
 * @param {React.ReactNode} children - The button's text or content.
 * @param {function} [onClick] - The function to call when the button is clicked.
 * @param {string} [className] - Optional additional CSS classes.
 */
const Button = ({ children, onClick, className = '' }) => (
  <button
    onClick={onClick}
    className={`w-full bg-teal-400 text-white font-bold py-3 px-6 rounded-lg hover:bg-teal-500 transition duration-300 shadow-md ${className}`}
  >
    {children}
  </button>
);

/**
 * A button that renders an icon, ensuring accessibility.
 * @param {React.ElementType} IconComponent - The icon component to render.
 * @param {string} label - The accessible label for the button.
 */
const IconButton = ({ IconComponent, label }) => (
  <button aria-label={label}>
    <IconComponent />
  </button>
);

/**
 * A checklist item with a completed or incomplete state.
 * @param {boolean} isCompleted - Determines if the checkmark is filled or empty.
 * @param {React.ReactNode} children - The text content of the checklist item.
 */
const ChecklistItem = ({ isCompleted, children }) => (
  <li className="flex items-center gap-3">
    {isCompleted ? <CompletedCheckIcon /> : <IncompleteCheckIcon />}
    <span className={`${isCompleted ? 'text-slate-600' : 'text-gray-400'} font-medium`}>
      {children}
    </span>
  </li>
);

/**
 * A circular progress bar component.
 * @param {number} percentage - The percentage to display (0-100).
 */
const CircularProgressBar = ({ percentage }) => {
  const radius = 45;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div className="relative w-40 h-40">
      <svg className="w-full h-full" viewBox="0 0 100 100">
        <circle
          className="text-gray-200"
          strokeWidth="10"
          stroke="currentColor"
          fill="transparent"
          r={radius}
          cx="50"
          cy="50"
        />
        <circle
          className="text-teal-400"
          strokeWidth="10"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          stroke="currentColor"
          fill="transparent"
          r={radius}
          cx="50"
          cy="50"
          transform="rotate(-90 50 50)"
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-3xl font-bold text-slate-700">{percentage}%</span>
      </div>
    </div>
  );
};

/**
 * Displays a team member's avatar and name.
 * @param {string} imageUrl - The URL for the team member's avatar.
 * @param {string} name - The name of the team member.
 */
const TeamMember = ({ imageUrl, name }) => (
  <div className="text-center">
    <img className="w-20 h-20 rounded-lg mx-auto object-cover" src={imageUrl} alt={name} />
    <p className="mt-2 font-semibold text-slate-700 text-sm">{name}</p>
  </div>
);

/**
 * Displays the user's profile avatar and name in the header.
 * @param {string} initials - The user's initials for the avatar.
 * @param {string} name - The user's full name.
 */
const UserProfile = ({ initials, name }) => (
  <div className="flex items-center gap-3">
    <div className="w-9 h-9 rounded-full bg-gray-200 flex items-center justify-center">
      <span className="font-bold text-slate-700">{initials}</span>
    </div>
    <span className="text-white font-medium hidden sm:block">{name}</span>
  </div>
);

// ================================================================================================
// 3. LAYOUT & SECTION COMPONENTS
// ================================================================================================

/**
 * The main header/navigation bar for the application.
 * @param {object} user - An object containing user information.
 */
const AppHeader = ({ user }) => (
  <header className="bg-slate-800 shadow-md">
    <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex items-center justify-between h-16">
        <div className="flex-shrink-0 flex items-center gap-3">
          <LogoWIcon />
          <span className="text-white text-xl font-semibold">WelcomePath</span>
        </div>
        <div className="flex items-center gap-5">
          <IconButton IconComponent={BellIcon} label="Notifications" />
          <IconButton IconComponent={BellIcon} label="Messages" />
          <UserProfile initials={user.initials} name={user.name} />
        </div>
      </div>
    </nav>
  </header>
);

/**
 * The welcome message section at the top of the main content.
 * @param {string} name - The name of the user to welcome.
 */
const WelcomeMessage = ({ name }) => (
  <section className="mb-10">
    <h1 className="text-4xl font-bold text-slate-800">Welcome, {name}!</h1>
    <p className="mt-2 text-lg text-slate-500">
      We're so excited to have you on the team. Here's your path to a great first week.
    </p>
  </section>
);

/**
 * The footer section with navigation links.
 */
const AppFooter = () => (
  <footer className="text-center mt-12 py-4">
    <nav className="flex justify-center items-center gap-6 sm:gap-8 text-sm">
      <a href="#" className="text-slate-600 font-bold hover:text-slate-900 transition-colors">Support</a>
      <a href="#" className="text-slate-500 hover:text-slate-900 transition-colors">Privacy Policy</a>
      <a href="#" className="text-slate-500 hover:text-slate-900 transition-colors">Terms of Service</a>
    </nav>
  </footer>
);

// ================================================================================================
// 4. MAIN PAGE COMPONENT
// ================================================================================================

// Mock data for demonstration purposes
const user = {
  name: "Alex Chen",
  initials: "AC",
};

const onboardingJourney = {
  progress: 25,
  tasks: [
    { text: "Setup your profile", completed: true },
    { text: "Complete HR paperwork", completed: false },
    { text: "Attend orientation", completed: false },
  ],
};

const firstTasks = {
  mainTask: "Complete HR Paperwork",
  subTasks: [
    { text: "Review company handbook", completed: true },
    { text: "Meet your buddy", completed: true },
  ],
};

const teamMembers = [
  { name: "Sarah Lee", imageUrl: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=128&h=128&q=80" },
  { name: "David Chen", imageUrl: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=128&h=128&q=80" },
  { name: "Maria Rodriguez", imageUrl: "https://images.unsplash.com/photo-1580489944761-15a19d654956?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=128&h=128&q=80" },
  { name: "Ben Carter", imageUrl: "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=128&h=128&q=80" },
];

/**
 * The main Onboarding Dashboard page component, composed of smaller, reusable sub-components.
 */
const OnboardingDashboard = () => {
  return (
    <div className="bg-gray-100 min-h-screen font-sans">
      <AppHeader user={user} />

      <main className="p-4 sm:p-6 lg:p-10">
        <div className="max-w-6xl mx-auto">
          <WelcomeMessage name={user.name.split(' ')[0]} />

          <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card title="Your Onboarding Journey">
              <div className="flex flex-col items-center justify-center my-4">
                <CircularProgressBar percentage={onboardingJourney.progress} />
              </div>
              <ul className="space-y-4 mt-4">
                {onboardingJourney.tasks.map((task) => (
                  <ChecklistItem key={task.text} isCompleted={task.completed}>
                    {task.text}
                  </ChecklistItem>
                ))}
              </ul>
            </Card>

            <Card title="Your First Tasks">
              <div className="space-y-4">
                <Button>{firstTasks.mainTask}</Button>
                <ul className="space-y-4 pt-2">
                  {firstTasks.subTasks.map((task) => (
                    <ChecklistItem key={task.text} isCompleted={task.completed}>
                      {task.text}
                    </ChecklistItem>
                  ))}
                </ul>
              </div>
            </Card>

            <Card title="Meet Your Team">
              <div className="grid grid-cols-2 gap-x-4 gap-y-6">
                {teamMembers.map((member) => (
                  <TeamMember key={member.name} name={member.name} imageUrl={member.imageUrl} />
                ))}
              </div>
            </Card>
          </section>
        </div>
      </main>

      <AppFooter />
    </div>
  );
};

export default OnboardingDashboard;

// Render the component to the DOM
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<OnboardingDashboard />);