Contributing to ClassroomPilot

Thank you for your interest in contributing to ClassroomPilot 🎓.
This document explains how to set up your environment, work with Git branches, and submit changes.

⸻

🖥 Development Setup
	1.	Fork this repository on GitHub.
	2.	Clone your fork locally:

git clone https://github.com/<your-username>/ClassroomPilot.git
cd ClassroomPilot


	3.	Add the upstream repository:

git remote add upstream https://github.com/hugo-valle/gh_classroom_tools.git


	4.	Always sync before starting new work:

git checkout develop
git pull upstream develop



⸻

🔀 Branching Workflow

We use a Gitflow-inspired branching strategy.
	•	main → Always stable, production-ready code.
	•	develop → Integration branch for ongoing development.
	•	feature/* → New features branch from develop.
	•	release/* → Prepares releases, branched from develop.
	•	hotfix/* → Urgent fixes, branched from main.

⸻

✅ Example Workflow

Creating a Feature Branch

git checkout develop
git pull upstream develop
git checkout -b feature/python-wrapper
git push origin feature/python-wrapper

Submitting Your Work
	1.	Commit and push your changes.
	2.	Open a Pull Request (PR) into develop.
	3.	Request at least 1 review (2 if targeting main).
	4.	Address feedback → merge when approved.

Release Process

git checkout develop
git checkout -b release/v1.0
git push origin release/v1.0

	•	Open PR into both main and develop.

Hotfix Process

git checkout main
git checkout -b hotfix/fix-bug-123
git push origin hotfix/fix-bug-123

	•	Open PR into both main and develop.

⸻

🔒 Branch Protection Rules

These rules are enforced in GitHub:
	•	main
	•	Requires 2 code reviews before merging.
	•	No direct pushes allowed.
	•	Status checks must pass.
	•	develop & release/*
	•	Require 1 code review.
	•	No direct pushes allowed.
	•	Status checks must pass.

⸻

📝 Code Style & Practices
	•	Follow PEP 8 (Python style guide).
	•	Keep commits focused and meaningful.
	•	Write clear PR descriptions.
	•	Add/update tests when introducing changes.
	•	Update docs if you add or change features.

⸻

🙌 Getting Help

If you’re unsure about anything:
	•	Open a Discussion on GitHub.
	•	Or start a Draft PR to gather early feedback.

⸻

🚀 With your help, ClassroomPilot will grow into a powerful open-source tool for educators!

⸻
