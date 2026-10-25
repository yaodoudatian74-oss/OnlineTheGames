# OnlineTheGames

オンラインのGames。バックエンドは Convex を使う。

## Convex 開発ルール

- 関数は `convex/` 配下に置く。新しい構文を使う: `query({ args, handler })` / `mutation(...)` / `action(...)`。
- 全ての関数に `args` のバリデータ(`v` from `convex/values`)を付ける。
- 外部公開しない関数は `internalQuery` / `internalMutation` / `internalAction` を使う。
- `filter` ではなく、`schema.ts` で `index` を定義して `withIndex` を使う。
- `query` / `mutation` からは外部 fetch をしない。必要なら `action` を使う。
- 関数の呼び出しは `api.*` / `internal.*`(`convex/_generated/api`)経由で行う。
- `convex/_generated/` は手で編集しない。
- スキーマは `convex/schema.ts` で `defineSchema` / `defineTable` を使って定義する。

## コマンド

- `npx convex dev` — 開発デプロイと同期(初回はログインが必要)
- `npx convex mcp start` — Convex MCP サーバー(`.mcp.json` に設定済み)
