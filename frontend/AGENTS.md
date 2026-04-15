# Frontend Agent Guide

## Purpose

This folder contains the MedTime Angular frontend for Sprint 1. The goal is to keep the app focused on a mobile-first UI with mocked data, ready to receive the backend API later.

## Stack

- Angular 21 with standalone components
- SCSS for styling
- No frontend backend integration yet
- No map button, map route, or location logic in Sprint 1

## Important Rules

- Keep the implementation mobile-first and visually close to the provided wireframe.
- Use mocked data/services that mirror the future API shape.
- Preserve the current route structure: units list, unit detail, attendance history, and profile placeholder.
- Avoid introducing a map feature, even as a stub button.
- Prefer small, focused components and simple service boundaries that can later be swapped for HTTP calls.
- Keep the codebase consistent with Angular standalone patterns.

## Expected UI Areas

- Units list screen for nearby hospitals
- Unit detail screen with waiting time and feedback
- Attendance history screen
- Profile placeholder screen
- Bottom navigation without a map item

## Verification

- Build must succeed with Angular CLI.
- Routes should load without backend calls.
- The UI should remain readable on mobile widths.
- Mocked data should be centralized in a service or fixture-like layer.
