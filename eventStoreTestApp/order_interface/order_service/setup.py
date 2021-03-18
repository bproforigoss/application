from setuptools import setup

setup(
    name="order_service",
    packages=["order_service"],
    include_package_data=True,
    install_requires=["flask", "prometheus_client", "requests"],
)
