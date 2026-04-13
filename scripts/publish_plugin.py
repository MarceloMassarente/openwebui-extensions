"""
Publish plugins to OpenWebUI Community
使用 OpenWebUICommunityClient 发布插件到官方社区

用法：
    python scripts/publish_plugin.py                              # 更新已发布的插件（版本变化时）
    python scripts/publish_plugin.py --force                      # 强制更新所有已发布的插件
    python scripts/publish_plugin.py --new plugins/actions/xxx    # 首次发布指定目录的新插件
    python scripts/publish_plugin.py --new plugins/actions/xxx --force  # 强制发布新插件
"""

import os
import sys
import re
import argparse

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from openwebui_community_client import get_client


def find_existing_plugins(plugins_dir: str) -> list:
    """查找所有已发布的插件文件（有 openwebui_id 的）"""
    plugins = []
    for root, dirs, files in os.walk(plugins_dir):
        # Exclude debug directory
        if "debug" in dirs:
            dirs.remove("debug")

        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read(2000)

                id_match = re.search(
                    r"(?:openwebui_id|post_id):\s*([a-z0-9-]+)", content
                )
                if id_match:
                    plugins.append(
                        {
                            "file_path": file_path,
                            "post_id": id_match.group(1).strip(),
                        }
                    )
    return plugins


def find_new_plugins_in_dir(target_dir: str) -> list:
    """查找指定目录中没有 openwebui_id 的新插件"""
    plugins = []

    if not os.path.isdir(target_dir):
        print(f"Error: {target_dir} is not a directory")
        return plugins

    for file in os.listdir(target_dir):
        if file.endswith(".py") and not file.startswith("__"):
            file_path = os.path.join(target_dir, file)
            if not os.path.isfile(file_path):
                continue

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read(2000)

            # 检查是否有 frontmatter (title)
            title_match = re.search(r"title:\s*(.+)", content)
            if not title_match:
                continue

            # 检查是否已有 ID
            id_match = re.search(r"(?:openwebui_id|post_id):\s*([a-z0-9-]+)", content)
            if id_match:
                print(f"  ⚠️  {file} already has ID, will update instead")
                plugins.append(
                    {
                        "file_path": file_path,
                        "title": title_match.group(1).strip(),
                        "post_id": id_match.group(1).strip(),
                        "is_new": False,
                    }
                )
            else:
                plugins.append(
                    {
                        "file_path": file_path,
                        "title": title_match.group(1).strip(),
                        "post_id": None,
                        "is_new": True,
                    }
                )

    return plugins


def main():
    parser = argparse.ArgumentParser(
        description="Publish plugins to OpenWebUI Market",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update existing plugins (with version check)
  python scripts/publish_plugin.py

  # Force update all existing plugins
  python scripts/publish_plugin.py --force

  # Publish only a specific plugin
  python scripts/publish_plugin.py --only plugins/tools/batch-install-plugins

  # Publish new plugins from a specific directory
  python scripts/publish_plugin.py --new plugins/actions/summary

  # Preview what would be done
  python scripts/publish_plugin.py --only plugins/tools/batch-install-plugins --dry-run
        """,
    )
    parser.add_argument(
        "--force", action="store_true", help="Force update even if version matches"
    )
    parser.add_argument(
        "--new",
        metavar="DIR",
        help="Publish new plugins from the specified directory (required for first-time publishing)",
    )
    parser.add_argument(
        "--only",
        metavar="PATH",
        help="Only publish a specific plugin file or directory (e.g. plugins/tools/batch-install-plugins)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually publishing",
    )
    args = parser.parse_args()

    try:
        client = get_client()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plugins_dir = os.path.join(base_dir, "plugins")

    updated = 0
    created = 0
    skipped = 0
    failed = 0

    # 处理 --only 参数：只更新指定的插件
    if args.only:
        target = args.only
        if not os.path.isabs(target):
            target = os.path.join(base_dir, target)

        # 如果是目录，查找该目录下的插件
        if os.path.isdir(target):
            print(f"📦 Publishing plugins from: {target}\n")
            plugins_to_publish = find_new_plugins_in_dir(target)
        # 如果是文件，直接处理
        elif os.path.isfile(target):
            print(f"📦 Publishing plugin: {os.path.basename(target)}\n")
            with open(target, "r", encoding="utf-8") as f:
                content = f.read(2000)
            title_match = re.search(r"title:\s*(.+)", content)
            id_match = re.search(r"(?:openwebui_id|post_id):\s*([a-z0-9-]+)", content)
            plugins_to_publish = [
                {
                    "file_path": target,
                    "title": title_match.group(1).strip() if title_match else os.path.basename(target),
                    "post_id": id_match.group(1).strip() if id_match else None,
                    "is_new": id_match is None,
                }
            ]
        else:
            print(f"Error: {target} not found")
            sys.exit(1)

        if not plugins_to_publish:
            print("No plugins found.")
            return

        for plugin in plugins_to_publish:
            file_path = plugin["file_path"]
            file_name = os.path.basename(file_path)
            title = plugin["title"]
            is_new = plugin.get("is_new", True)

            if is_new:
                print(f"🆕 Creating: {file_name} ({title})")
            else:
                print(f"📦 Updating: {file_name} (ID: {plugin['post_id'][:8]}...)")

            if args.dry_run:
                print(f"  [DRY-RUN] Would {'create' if is_new else 'update'}")
                continue

            success, message = client.publish_plugin_from_file(
                file_path, force=args.force, auto_create=True
            )

            if success:
                if "Created" in message:
                    print(f"  🎉 {message}")
                    created += 1
                elif "Skipped" in message:
                    print(f"  ⏭️  {message}")
                    skipped += 1
                else:
                    print(f"  ✅ {message}")
                    updated += 1
            else:
                print(f"  ❌ {message}")
                failed += 1

    # 处理新插件发布
    elif args.new:
        target_dir = args.new
        if not os.path.isabs(target_dir):
            target_dir = os.path.join(base_dir, target_dir)

        print(f"🆕 Publishing new plugins from: {target_dir}\n")
        new_plugins = find_new_plugins_in_dir(target_dir)

        if not new_plugins:
            print("No plugins found in the specified directory.")
            return

        for plugin in new_plugins:
            file_path = plugin["file_path"]
            file_name = os.path.basename(file_path)
            title = plugin["title"]
            is_new = plugin.get("is_new", True)

            if is_new:
                print(f"🆕 Creating: {file_name} ({title})")
            else:
                print(f"📦 Updating: {file_name} (ID: {plugin['post_id'][:8]}...)")

            if args.dry_run:
                print(f"  [DRY-RUN] Would {'create' if is_new else 'update'}")
                continue

            success, message = client.publish_plugin_from_file(
                file_path, force=args.force, auto_create=True
            )

            if success:
                if "Created" in message:
                    print(f"  🎉 {message}")
                    created += 1
                elif "Skipped" in message:
                    print(f"  ⏭️  {message}")
                    skipped += 1
                else:
                    print(f"  ✅ {message}")
                    updated += 1
            else:
                print(f"  ❌ {message}")
                failed += 1

    # 处理已有插件更新
    else:
        existing_plugins = find_existing_plugins(plugins_dir)
        print(f"Found {len(existing_plugins)} existing plugins with OpenWebUI ID.\n")

        if not existing_plugins:
            print("No existing plugins to update.")
            print(
                "\n💡 Tip: Use --new <dir> to publish new plugins from a specific directory"
            )
            return

        for plugin in existing_plugins:
            file_path = plugin["file_path"]
            file_name = os.path.basename(file_path)
            post_id = plugin["post_id"]

            print(f"📦 {file_name} (ID: {post_id[:8]}...)")

            if args.dry_run:
                print(f"  [DRY-RUN] Would update")
                continue

            success, message = client.publish_plugin_from_file(
                file_path, force=args.force, auto_create=False  # 不自动创建，只更新
            )

            if success:
                if "Skipped" in message:
                    print(f"  ⏭️  {message}")
                    skipped += 1
                else:
                    print(f"  ✅ {message}")
                    updated += 1
            else:
                print(f"  ❌ {message}")
                failed += 1

    print(f"\n{'='*50}")
    print(
        f"Finished: {created} created, {updated} updated, {skipped} skipped, {failed} failed"
    )


if __name__ == "__main__":
    main()
