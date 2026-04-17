# sqlite3-native-library

SQLite3 的 HarmonyOS 原生库，与 [simolus3/sqlite-native-libraries](https://github.com/simolus3/sqlite-native-libraries/blob/master/sqlite3-native-library/cpp/CMakeLists.txt) 的编译选项保持一致。

本库的首个发布版本为 `3.46.0` 。自该版本起，本库版本号与 SQLite 一一对应，例如 `"sqlite3-native-library": "^3.46.0"` 即对应 [SQLite 3.46.0](https://sqlite.org/releaselog/3_46_0.html)。

用于 [sqlite3-ohos.dart](https://github.com/SageMik/sqlite3-ohos.dart)，基于 [Flutter 鸿蒙适配版](https://gitcode.com/openharmony-tpc/flutter_flutter) 为 Flutter 访问 SQLite3 提供 HarmonyOS 支持。

```shell
ohpm install sqlite3-native-library
```