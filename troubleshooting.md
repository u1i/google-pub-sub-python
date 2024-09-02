# Troubleshooting Google Cloud Service Account Issues

This guide provides solutions to common issues you might encounter when creating and configuring service accounts for use with Google Cloud Pub/Sub.

## Common Issues

### 1. Permission Denied: 403 Error

#### Error Message
```
google.api_core.exceptions.PermissionDenied: 403 Caller does not have required permission to use project [project-id]. Grant the caller the roles/serviceusage.serviceUsageConsumer role, or a custom role with the serviceusage.services.use permission.
```

#### Solution
Ensure the `roles/serviceusage.serviceUsageConsumer` role is assigned to the service account.

**Command to Grant Role**:
```
gcloud projects add-iam-policy-binding [your-project-id] \
    --member="serviceAccount:[service-account-email]" \
    --role="roles/serviceusage.serviceUsageConsumer"
```

### 2. Failed Precondition: Key Creation Not Allowed

#### Error Message
```
ERROR: (gcloud.iam.service-accounts.keys.create) FAILED_PRECONDITION: Key creation is not allowed on this service account.
```

#### Solution
This issue is due to the policy constraint `constraints/iam.disableServiceAccountKeyCreation`. Here’s how to handle it:

1. **Check the Policy Constraint**:
    ```
    gcloud org-policies describe constraints/iam.disableServiceAccountKeyCreation --organization=[your-organization-id]
    ```

2. **Update Policy to Temporarily Disable Enforcement**:
   Create a policy configuration file `iam_disable_key_creation_policy.yaml`:

    ```
    etag: [corresponding-etag]
    name: organizations/[your-organization-id]/policies/iam.disableServiceAccountKeyCreation
    spec:
      rules:
      - enforce: false
    ```

3. **Apply the Policy**:
    ```
    gcloud org-policies set-policy iam_disable_key_creation_policy.yaml
    ```

4. **Create the Service Account Key**:
    ```
    gcloud iam service-accounts keys create ~/keyfile.json \
        --iam-account=[service-account-email]
    ```

5. **Re-enable the Policy**:
   Update the policy file to re-enable the constraint after key creation:

    ```
    etag: [new-etag]
    name: organizations/[your-organization-id]/policies/iam.disableServiceAccountKeyCreation
    spec:
      rules:
      - enforce: true
    ```

    **Apply the Updated Policy**:
    ```
    gcloud org-policies set-policy iam_disable_key_creation_policy.yaml
    ```

### 3. Service Account Already Exists

#### Error Message
```
ERROR: (gcloud.iam.service-accounts.create) Resource in projects [project-id] is the subject of a conflict: Service account [service-account-name] already exists within project.
```

#### Solution
Verify the service account exists using:
```
gcloud iam service-accounts list
```

If the account exists, skip the creation step and proceed with assigning roles or creating keys as needed.

### 4. Missing Permissions for Subscription or Publishing

#### Error Message
```
google.api_core.exceptions.PermissionDenied: 403 User does not have permission to perform this action.
```

#### Solution
Ensure the service account has both `roles/pubsub.publisher` and `roles/pubsub.subscriber` roles.

**Command to Grant Roles**:
```
gcloud projects add-iam-policy-binding [your-project-id] \
    --member="serviceAccount:[service-account-email]" \
    --role="roles/pubsub.publisher"

gcloud projects add-iam-policy-binding [your-project-id] \
    --member="serviceAccount:[service-account-email]" \
    --role="roles/pubsub.subscriber"
```

## General Tips

1. **Ensure API is Enabled**:
    ```
    gcloud services enable pubsub.googleapis.com
    ```

2. **Verify IAM Policy Bindings**:
    ```
    gcloud projects get-iam-policy [your-project-id] --filter="bindings.members:[service-account-email]"
    ```

3. **Check Service Account Details**:
    ```
    gcloud iam service-accounts describe [service-account-email]
    ```

4. **Propagation Time**:
   Permissions and policy changes may take a few minutes to propagate. Wait a while and retry if changes do not take effect immediately.

By following these troubleshooting steps, you should be able to resolve common issues with service account creation and configuration for Google Cloud Pub/Sub. If the problem persists, consult Google's [official documentation](https://cloud.google.com/iam/docs/) or support channels.