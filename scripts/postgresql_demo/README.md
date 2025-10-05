## Installation Guide- PGVector

Mac/Linux

```
cd /tmp 
git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git 
cd pgvector
export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"
```

Or 

```
brew install postgresql@16 
export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"
```

> Start the Service first: 

```
brew services start postgresql@16 
```

## Verify

> To test the connection: psql postgres
> Vector extension: ls /opt/homebrew/opt/postgresql@16/share/postgresql@16/extension/vector*

### Create Vector Extension

- CREATE EXTENSION vector 
- \dx vector

Then, Create a Server on PGAdmin

```
brew install --cask pgadmin4
```

## Resources:

- [PGVector - GitHub](https://github.com/pgvector/pgvector)
- [PGAdmin-4 UI](https://www.pgadmin.org/docs/pgadmin4/development/user_interface.html)