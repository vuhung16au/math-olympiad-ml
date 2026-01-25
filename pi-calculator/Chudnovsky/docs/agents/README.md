# Agent Coding Guidelines

This document outlines the coding standards and best practices for development in this project.

## Overview

These guidelines are organized into policy categories. Each category contains specific principles, guidelines, and implementation examples.

## Policy Categories

1. **[Multi-Threading](multi-threading.md)** - Guidelines for concurrent programming with goroutines
2. **[Multi-Core Utilization](multi-core.md)** - Strategies for leveraging all available CPU cores
3. **[Modular Architecture](modular-architecture.md)** - Principles for organizing code into reusable modules
4. **[Object-Oriented Programming](oop.md)** - OOP practices and SOLID principles
5. **[File Size Management](file-size-management.md)** - Guidelines for keeping files under 500 lines
6. **[Security](security.md)** - Protection against common vulnerabilities
7. **[Best Practices](best-practices.md)** - General coding best practices

## Quick Reference

- **Performance First**: Always consider parallelization opportunities
- **Code Organization**: Keep files small and focused
- **Reusability**: Design components to be reusable
- **Testability**: Write testable, modular code
- **Documentation**: Document public APIs and complex logic
- **Error Handling**: Handle errors explicitly and gracefully
- **Security**: Always validate input, check bounds, and protect against common vulnerabilities

## Notes

- These guidelines should be followed whenever practical
- Some exceptions may be necessary for specific use cases
- Always prioritize correctness over performance optimizations
- Profile and measure before optimizing
