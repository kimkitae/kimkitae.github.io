---
layout: post
title: "Mobile Automation Journey: From Appium to API-Assisted Tests"
author: KimKitae
date: 2024-07-28 11:42:00 +0900
last_modified_at: 2026-11-08
lang: en
permalink: /en/posts/mobile-automation/
translation_url: /posts/mobile-automation/
description: Lessons from a decade of mobile automation, from Appium and parallel devices to Espresso, XCUITest, Katalon, and API-assisted testing.
categories: [Automation, Testing]
tags: [Testing, Appium, Espresso]
---

After nearly a decade of mobile automation, I care less about the tool and more about two questions: what should be automated, and how quickly can a failure be explained? This is not a collection of success stories. It is a chronological record of problems I hit and the workarounds I chose. My current judgment is not always the same as it was at the time.

![Timeline from Appium black-box tests to native frameworks, Katalon, and API-assisted automation](/assets/img/posts/renewal/mobile-automation.svg)

*Figure 1. The four stages I went through. Each stage was chosen to reduce a failure mode from the previous one.*

## Starting with Appium

I first met Appium in 2014. What stood out was that it worked through code and a CLI rather than a GUI recorder. With very little Korean-language material available, it took a long time to make even one Android device reliable. Later I ran four or more devices in parallel through Parallels, collected results, and attached the process to the release workflow.

At a commerce QA team in 2018, I used Appium again across Android and iOS and connected builds and tests through Jenkins. At the time, “the tests run” felt like a success. Once we operated them, other problems appeared.

## Repeated failures from resource IDs

The most common failure was a missing or changed resource ID. Appium fails at the step where a locator is missing, but in our setup we only learned which screen had broken after the whole suite ran and the results were collected. We then inspected the failure, fixed the ID, and reran everything before getting a meaningful result. The longer the feedback loop, the harder it was to trust the automation.

So we moved to Espresso on Android and XCUITest on iOS. With the white-box approach, the ids our tests referenced were visible in the app source, so our build caught missing or changed ids earlier. That still did not catch arbitrary string locator changes at compile time; what the build caught depended on the configuration and on how the tests were written. The change contributed to shortening the release cycle from once every two weeks to once a week. But it required maintenance at the same pace as development, and access restrictions and difficulty meant not every QA engineer could write the tests. That limitation led us to Katalon.

## Katalon and page objects

Katalon was built on Appium but allowed people to write scenarios with little code. By grouping screen-specific functions into page objects, team members with less automation experience could create scenarios. Converting the existing code took about a month, and we expanded coverage quickly. The tool did not remove the problems, but it widened the set of people who could write tests.

## Experiments with APIs and AI

Around the time I wrote this in 2024, as business logic moved to the backend, preparing state through an API became more efficient than driving every step through the UI. We generated data in the same shape the client receives, used the UI only where visual confirmation mattered, and reduced dependence on resource IDs.

The original 2024 post says GPT was used to compare page sources and suggest selector fixes, and that existing scripts were used to generate scenario scripts, raising productivity. That was the assessment at the time. Current advice is different: treat automatic repair as a way to propose likely causes rather than a replacement for deterministic automation, and confirm the final judgment with a reproducible test. Image-based vision belongs in the same category: a supporting signal, not the foundation. The foundation is still reproducible state setup and clear failure messages.
