# kong-core

[![NPM version](https://badge.fury.io/js/kong-core.svg)](https://badge.fury.io/js/kong-core)
[![PyPI version](https://badge.fury.io/py/kong-core.svg)](https://badge.fury.io/py/kong-core)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/kong-core?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/kong-core?label=pypi&color=blue)

Use this Kong CDK Construct Library to deploy Core common infrastructural constructs .

This CDK library automatically creates and configures recommended architecture on AWS by:

* *Amazon EKS*

  * Well architected EKS cluster from networking standpoint
  * Cluster autoscaler
  * Node termination handler
  * Secrets management from AWS Secrets Manager using CSI driver
  * mTLS using AWS ACM for pod to pod communication using private certificate authority and aws-pca-issuer
  * Use of IAM Role for Service Account (IRSA) where applicable
  * AWS EKS encryption at rest
  * Metrics server installation
  * Logs and metrics to cloudwatch using AWS CloudWatch Container insights
* *Elasticache*

  * private accessibility
  * multi az
  * auto failover
  * auto minor version upgrade
  * cwl output
* *RDS Features*

  * Encryption at rest
  * Private subnets
  * Multiaz
  * auto backup
  * Logs output to CloudWatch

## npm Package Installation:

```
yarn add --dev kong-core
# or
npm install kong-core --save-dev
```

## PyPI Package Installation:

```
pip install kong-core
```

# Sample

Try out https://github.com/kong/aws-samples for the complete sample application and instructions.

## Resources to learn about CDK

* [CDK TypeScript Workshop](https://cdkworkshop.com/20-typescript.html)
* [Video Introducing CDK by AWS with Demo](https://youtu.be/ZWCvNFUN-sU)
* [CDK Concepts](https://youtu.be/9As_ZIjUGmY)

## Related

Kong on AWS Hands on Workshop - https://kong.awsworkshop.io/

## Useful commands

* `rm -rf node_modules && rm package.json && rm package-lock.json && rm yarn.lock && rm tsconfig.dev.json` cleans the directory
* `npm install projen` installs projen
* `npx projen build`   Test + Compile + Build JSII packages
* `npx projen watch`   compile and run watch in background
* `npm run test`    perform the jest unit tests

## Tips

* Use a locked down version of `constructs` and `aws-cdk-lib`. Even with CDK V2 i saw https://github.com/aws/aws-cdk/issues/542 repeating when there is minor version mismatch of construcs. AWS CDK init commands generate package.json file without locked down version of constructs library.
