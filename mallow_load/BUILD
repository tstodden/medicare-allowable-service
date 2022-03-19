load("@rules_python//python:python.bzl", "py_library")
load("@io_bazel_rules_docker//python3:image.bzl", "py3_image")

py_library(
    name = "lib",
    srcs = glob(["mallow_load/**/*.py"]),
    deps = ["//requirements:deps"],
)

py3_image(
    name = "app",
    srcs = ["main.py"],
    main = "main.py",
    deps = [":lib"],
)
