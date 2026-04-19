# 🤝 Contributing to AI Clipper

Thank you for your interest in contributing to AI Clipper! We welcome contributions from developers, designers, and users of all skill levels.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)

---

## 🌟 Code of Conduct

### Our Pledge

We are committed to making participation in our project a harassment-free experience for everyone, regardless of level of experience, gender, gender identity and expression, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, religion, or nationality.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Harassment, trolling, or disrespectful comments
- Personal or political attacks
- Public or private harassment
- Publishing others' private information
- Other unethical or unprofessional conduct

---

## 🚀 Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Git** - Version control
- **Node.js** (v18+) - Frontend development
- **Rust** (stable) - Tauri development
- **Python** (3.11+) - Backend development
- **FFmpeg** - Video processing

### Fork the Repository

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-clipper.git
   cd ai-clipper
   ```

3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/ai-clipper.git
   ```

---

## 💻 Development Setup

### Frontend (React + Tauri)

```bash
cd frontend
npm install
npm run tauri:dev
```

### Backend (Python)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Running Full Stack

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run tauri:dev
```

---

## 📝 Contributing Guidelines

### Types of Contributions

We welcome contributions in many forms:

1. **Bug Fixes** - Fix reported issues
2. **New Features** - Add new functionality
3. **Documentation** - Improve docs and guides
4. **Tests** - Add or improve tests
5. **Performance** - Optimize code
6. **UI/UX** - Improve design and user experience
7. **Translations** - Add language support

### Before You Start

1. **Check for existing issues**
   - Search open issues to avoid duplicates
   - Comment on existing issue to discuss

2. **Create an issue** (for new features)
   - Describe the feature
   - Explain the use case
   - Discuss approach

3. **Get approval**
   - Wait for maintainer response
   - Discuss implementation details
   - Ensure it aligns with project goals

---

## 🔀 Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

**Branch Naming:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `test/` - Test additions
- `refactor/` - Code refactoring

### 2. Make Changes

- Write clean, well-documented code
- Follow coding standards (see below)
- Add tests for new features
- Update documentation
- Test thoroughly

### 3. Commit Changes

```bash
git add .
git commit -m "feat: add new feature"
# or
git commit -m "fix: resolve bug in video processing"
```

**Commit Message Format:**
```
type(scope): subject

body

footer
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style (formatting, etc.)
- `refactor` - Code refactoring
- `test` - Test additions/changes
- `chore` - Maintenance tasks

**Examples:**
```
feat(ui): add dark mode toggle

Implement a toggle button in settings panel to switch between
light and dark themes. Persists preference to local storage.

Closes #123
```

```
fix(api): resolve crash when processing long videos

The application would crash when processing videos longer than
2 hours due to buffer overflow. Added proper validation and
error handling.

Fixes #456
```

### 4. Sync with Upstream

```bash
git fetch upstream
git rebase upstream/main
```

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title describing the change
- Detailed description of what was changed
- Link to related issue(s)
- Screenshots (for UI changes)
- Testing instructions

### 6. Respond to Feedback

- Address reviewer comments
- Make requested changes
- Keep PR up-to-date
- Be responsive and polite

---

## 📐 Coding Standards

### Frontend (React + TypeScript)

**File Structure:**
```
src/
├── components/
│   ├── ComponentName/
│   │   ├── ComponentName.tsx
│   │   ├── index.ts
│   │   └── types.ts
├── hooks/
│   └── useHookName.ts
├── services/
│   └── serviceName.ts
├── types/
│   └── api.ts
├── utils/
│   └── helpers.ts
└── styles/
    └── globals.css
```

**Component Template:**
```tsx
import React, { useState, useEffect } from 'react';

interface ComponentNameProps {
  prop1: string;
  prop2?: number;
}

/**
 * ComponentName - Brief description
 *
 * @param prop1 - Description
 * @param prop2 - Description (optional)
 */
export default function ComponentName({
  prop1,
  prop2 = 0
}: ComponentNameProps) {
  const [state, setState] = useState<string>('');

  useEffect(() => {
    // Effect logic
  }, [dependency]);

  return (
    <div className="component-name">
      {/* JSX */}
    </div>
  );
}
```

**Best Practices:**
- Use functional components with hooks
- Define interfaces for props
- Add JSDoc comments for complex functions
- Use TypeScript strictly
- Keep components small and focused
- Follow naming conventions: PascalCase for components

### Backend (Python)

**File Structure:**
```
backend/
├── api/
│   └── endpoint.py
├── services/
│   └── service_name.py
├── models/
│   └── model_name.py
├── utils/
│   └── helpers.py
└── main.py
```

**Function Template:**
```python
def function_name(param1: str, param2: int = 0) -> bool:
    """
    Brief description of function.

    Args:
        param1: Description of param1
        param2: Description of param2 (default: 0)

    Returns:
        bool: Description of return value

    Raises:
        ValueError: If param1 is invalid
    """
    # Implementation
    return True
```

**Best Practices:**
- Use type hints
- Write docstrings for functions
- Follow PEP 8 style guide
- Use meaningful variable names
- Handle errors properly
- Write unit tests

### General Guidelines

**Git:**
- Commit often, in small chunks
- Write clear commit messages
- Don't commit sensitive data (API keys, etc.)
- Use `.gitignore` properly

**Documentation:**
- Update README for user-facing changes
- Update API docs for API changes
- Add comments for complex logic
- Keep docs in sync with code

**Testing:**
- Write tests for new features
- Ensure existing tests pass
- Test on multiple platforms if possible
- Add test cases for edge cases

---

## 🐛 Reporting Issues

### Before Reporting

1. **Search existing issues**
   - Check if issue already reported
   - Add to existing issue if relevant

2. **Gather information**
   - Version of AI Clipper
   - Operating system
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/screenshots

### Issue Template

```markdown
**Description:**
[Brief description of the issue]

**Steps to Reproduce:**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior:**
[What you expected to happen]

**Actual Behavior:**
[What actually happened]

**Environment:**
- OS: [e.g., Windows 11]
- AI Clipper Version: [e.g., 1.0.0]
- Python Version: [e.g., 3.11]
- Node Version: [e.g., 18.17.0]

**Logs/Error Messages:**
```
[Paste error logs here]
```

**Screenshots (if applicable):**
[Attach screenshots]

**Additional Context:**
[Any additional information]
```

---

## 💡 Feature Requests

### Before Requesting

1. **Check roadmap**
   - See if feature is already planned
   - Check `ROADMAP.md`

2. **Search issues**
   - Look for similar requests
   - Comment on existing request

### Request Template

```markdown
**Feature Title:**
[Concise title for the feature]

**Problem:**
[Describe the problem you're trying to solve]

**Proposed Solution:**
[Describe the solution you have in mind]

**Alternatives Considered:**
[Describe alternative solutions you've considered]

**Additional Context:**
[Any additional context, screenshots, examples, etc.]

**Would you like to work on this?**
[Yes/No/Maybe]
```

---

## 🎨 Design Contributions

### UI/UX Improvements

- Create mockups or wireframes
- Explain user experience improvements
- Consider accessibility
- Keep consistent with existing design

### Assets

- Icons should be SVG format
- Images should be optimized
- Follow brand guidelines
- Use consistent color schemes

---

## 🌍 Translations

### Adding New Language

1. Create language file: `locales/XX.json`
2. Translate all strings
3. Update language list in settings
4. Test thoroughly

**Format:**
```json
{
  "common": {
    "save": "Save",
    "cancel": "Cancel"
  },
  "ui": {
    "title": "AI Clipper",
    "generate": "Generate Clips"
  }
}
```

---

## 📊 Performance

### Optimization Guidelines

- Profile before optimizing
- Benchmark improvements
- Document performance gains
- Consider trade-offs

### Areas of Focus

- Video processing speed
- Memory usage
- Startup time
- UI responsiveness

---

## 🏆 Recognition

**Contributors will be:**
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Invited to contributor discussions
- Eligible for contributor badge

---

## ❓ Questions?

- **GitHub Discussions:** Ask questions here
- **Email:** dev@example.com
- **Discord:** Join our server (coming soon)

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

We appreciate every contribution, no matter how small. Thank you for helping make AI Clipper better!

---

**Made with ❤️ by the AI Clipper Team**
**Together we build great software! 🚀**
