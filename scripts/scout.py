import os
import anthropic
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))


def generate_report() -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    today = datetime.now(JST).strftime("%Y年%m月%d日")

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": f"""今週（{today}時点）の熱海市の中古マンション市場について、以下の観点でレポートを作成してください。

## レポート内容
1. **市場動向サマリー**：熱海の不動産市場の現状
2. **注目エリア**：海近・駅近など人気エリアの特徴
3. **価格帯の目安**：一般的な中古マンションの価格レンジ
4. **購入チェックポイント**：熱海物件特有の注意点（温泉権、管理費など）
5. **今週のアドバイス**：購入・投資タイミングの考察

マークダウン形式で、実用的で読みやすいレポートを作成してください。""",
            }
        ],
    )

    return message.content[0].text


def main():
    now = datetime.now(JST)
    report_content = generate_report()

    header = f"# 熱海中古マンション週次レポート\n\n生成日時：{now.strftime('%Y年%m月%d日 %H:%M')} JST\n\n---\n\n"
    full_report = header + report_content

    os.makedirs("reports", exist_ok=True)
    filename = f"reports/report_{now.strftime('%Y%m%d')}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(full_report)

    print(f"レポートを保存しました: {filename}")


if __name__ == "__main__":
    main()
