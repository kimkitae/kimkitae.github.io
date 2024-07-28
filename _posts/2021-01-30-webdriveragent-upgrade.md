---
title: iOS 14+, WebDriverAgent 업데이트
author: KimKitae
description: >-
  APPIUM iOS 최신버전을 위한 old iOS 버전에서 WebdriverAgent 업데이트
date: 2021-01-30 00:34:00 +0800
categories: [Automation, iOS]
tags: [Automation, iOS]
---

최신 iOS 14.4로 업데이트가 되어 기존 WebDriverAgent로는 지원이 되지 않아 지원 가능한 최신버전으로 업데이트가 필요 했습니다. 자동화 프로젝트로 인해 기존 APPIUM의 버전은 그대로 두고 WebDriverAgent 의 버전만 필요하였습니다.

```shell
xcodebuild failure: Command '/bin/bash /usr/local/lib/node_modules/appium/node_modules/appium-webdriveragent/Scripts/carthage-wrapper.sh bootstrap --platform iOS\,tvOS' exited with code 1. Make sure you follow the tutorial at https://github.com/appium/appium-xcuitest-driver/blob/master/docs/real-device-config.md. Try to remove the WebDriverAgentRunner application from the device if it is installed and reboot the device.
```

 [appium/WebDriverAgent](https://github.com/appium/WebDriverAgent) 에서 파일을 다운로드하여 기존 appium-webdriveragent를 교체를 하면 됩니다만 해당 폴더 안에 `carthage` 관련 파일이 없기 때문에 기존 폴더에 있는 `Carthage` 폴더, `Scripts 폴더 내 carthage.sh` 와 `Cartfile`, `Cartfile.resolved` 파일을 복사 해두었다가 새로 교체 후 기존에 가져온 경로와 동일하게 붙여 놓습니다.

```shell
./Scripts/carthage-wrapper.sh bootstrap --platform iOS\,tvOS
```

위 커맨드를 실행하게 되면 빌드에 필요한 파일들을 다운로드 완료가 됩니다.

```shell
appium-webdriveragent ./Scripts/carthage-wrapper.sh bootstrap --platform iOS\,tvOS
Applying Carthage build workaround to exclude Apple Silicon binaries. See https://github.com/Carthage/Carthage/issues/3019 for more details
*** Checking out CocoaAsyncSocket at "72e0fa9e62d56e5bbb3f67e9cfd5aa85841735bc"
*** Checking out YYCache at "1.1.2"
*** xcodebuild output can be found in /var/folders/8h/s56hq5_d5f70bjc3p3x1kgv9234mt2/T/carthage-xcodebuild.FsfAiB.log
*** Building scheme "tvOS Framework" in CocoaAsyncSocket.xcodeproj
*** Building scheme "iOS Framework" in CocoaAsyncSocket.xcodeproj
*** Building scheme "YYCache tvOS" in YYCache.xcodeproj
*** Building scheme "YYCache iOS" in YYCache.xcodeproj
```



