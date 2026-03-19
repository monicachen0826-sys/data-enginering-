# ISS Location Tracker - OpenShift Deployment

Minimal Python cronjob that polls the ISS Space Station API and stores location data in PostgreSQL.

## Files

- `iss_poller.py` - Python script that fetches ISS location and stores in database
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container image for the Python app
- `init.sql` - Database schema initialization
- `postgres-pvc.yaml` - Persistent volume claim for database storage
- `postgres-configmap.yaml` - Database initialization script
- `postgres-deployment.yaml` - PostgreSQL deployment
- `postgres-service.yaml` - PostgreSQL service
- `iss-poller-cronjob.yaml` - ISS poller cronjob

## Database Schema

- **Table**: `iss_locations`
- **Columns**: id, latitude, longitude, timestamp, recorded_at
- **Storage**: 1GB PostgreSQL Alpine
- **Credentials**: postgres/postgres (default)

## Deployment Steps

### 1. Login to OpenShift

```bash
oc login <your-openshift-cluster-url>
```

### 2. Create a New Project

```bash
oc new-project iss-tracker
```

### 3. Build the ISS Poller Image

```bash
oc new-build --name=iss-poller --binary --strategy=docker
oc start-build iss-poller --from-dir=. --follow
```

### 4. Deploy Resources

```bash
oc apply -f postgres-pvc.yaml
oc apply -f postgres-configmap.yaml
oc apply -f postgres-deployment.yaml
oc apply -f postgres-service.yaml
oc apply -f iss-poller-cronjob.yaml
```

Or deploy all at once:

```bash
oc apply -f .
```

### 5. Verify Deployment

Check PostgreSQL pod:

```bash
oc get pods -l app=postgres
```

Check cronjob:

```bash
oc get cronjobs
```

View cronjob runs:

```bash
oc get jobs
```

Check logs:

```bash
oc logs -l job-name=<job-name>
```

### 6. Query the Database

Connect to PostgreSQL:

```bash
oc exec -it deployment/postgres -- psql -U postgres -d issdb
```

Query ISS locations:

```sql
SELECT * FROM iss_locations ORDER BY recorded_at DESC LIMIT 10;
```

## Configuration

The cronjob runs every 5 minutes (`*/5 * * * *`). To change frequency, edit the `schedule` field in `iss-poller-cronjob.yaml`.

## Clean Up

```bash
oc delete -f iss-poller-cronjob.yaml
oc delete -f postgres-service.yaml
oc delete -f postgres-deployment.yaml
oc delete -f postgres-configmap.yaml
oc delete -f postgres-pvc.yaml
oc delete bc/iss-poller
oc delete is/iss-poller
```

Or delete all at once:

```bash
oc delete -f .
oc delete bc/iss-poller
oc delete is/iss-poller
```

Or delete the entire project:

```bash
oc delete project iss-tracker
```
