# Sudoku – Professional Edition

## English

### Overview
**Sudoku – Professional Edition** is a modern, feature-rich desktop Sudoku game built with **Python** and **PyQt6**. It offers a polished Windows 11-inspired interface, real-time validation, multilingual support, dynamic theming, and intelligent puzzle generation — perfect for casual players and puzzle enthusiasts alike.

### Key Features
- **9×9 Interactive Grid**: Large, responsive cells with **real-time input validation** and **visual feedback**.
- **Smart Puzzle Generator**: Creates valid, unique puzzles using **backtracking algorithm** with 4 difficulty levels.
- **Live Progress Tracking**:
  - **Timer** (MM:SS)
  - **Mistakes counter** (max 3)
  - **Smooth progress bar**
- **Instant Feedback**:
  - Correct entries → **Blue**
  - Wrong entries → **Red**
  - Hints → **Green**
- **Hint System**: One-click reveal of any empty cell.
- **Check Solution**: Verify current board without solving.
- **Multilingual UI**: Full support for **English**, **فارسی (RTL)**, **中文**, and **Русский**.
- **5 Elegant Themes**:
  - Windows Default
  - Light
  - Dark
  - Blue
  - Red
- **RTL Layout Support**: Automatic right-to-left for Persian.
- **Game Over Detection**: Ends game after 3 mistakes.
- **Victory Celebration**: Shows time and hints used upon completion.

### Requirements
- Python 3.8+
- PyQt6

### Installation
1. Ensure Python is installed.
2. Install dependency:
   ```bash
   pip install PyQt6
   ```
3. Run the game:
   ```bash
   python sudoku.py
   ```

### Usage
- **Start Playing**: Fill empty cells with numbers 1–9.
- **Select Difficulty**: Easy → Expert via dropdown.
- **Use Hint**: Click **Hint** to reveal one cell.
- **Check Progress**: Click **Check** to validate.
- **New Game**: Start fresh anytime.
- **Change Language/Theme**: Use header selectors.

### Screenshots
- Clean header with difficulty, language & theme controls  
- Responsive 9×9 grid with thick 3×3 block borders  
- Persian RTL interface with full translation  
- Dark theme with high-contrast input states  
- Victory dialog with time and hint stats  
- Real-time mistake counter and progress bar  

### Technical Highlights
- **Backtracking Solver**: Generates and solves puzzles efficiently.
- **Custom QLineEdit**: `SudokuCell` with validation, styling, and shadows.
- **Dynamic Theming**: Full palette + stylesheet control.
- **Signal-Driven Architecture**: Clean separation of logic and UI.
- **Difficulty Scaling**: Removes 45–60 cells based on level.
- **Cross-Platform**: Works on Windows, macOS, and Linux.

### Contributing
Fork and improve: add undo/redo, pencil marks, daily challenges, or export to PDF. Pull requests welcome!

### License
MIT License – Free for personal, educational, and commercial use.

---

## فارسی

### بررسی اجمالی
**سودوکو – نسخه حرفه‌ای** یک بازی دسکتاپ مدرن و پرامکانات است که با **پایتون** و **PyQt6** ساخته شده. این برنامه با رابط کاربری الهام‌گرفته از ویندوز ۱۱، اعتبارسنجی لحظه‌ای، پشتیبانی چندزبانه، تم‌های پویا و تولید هوشمند پازل، تجربه‌ای ایده‌آل برای بازیکنان معمولی و علاقه‌مندان به پازل ارائه می‌دهد.

### ویژگی‌های کلیدی
- **شبکه ۹×۹ تعاملی**: خانه‌های بزرگ و پاسخگو با **اعتبارسنجی لحظه‌ای** و **بازخورد بصری**.
- **تولیدکننده هوشمند پازل**: ایجاد پازل‌های معتبر و یکتا با الگوریتم **بازگشت** در ۴ سطح دشواری.
- **پیگیری پیشرفت زنده**:
  - **تایمر** (دقیقه:ثانیه)
  - **شمارنده اشتباهات** (حداکثر ۳)
  - **نوار پیشرفت نرم**
- **بازخورد فوری**:
  - ورودی درست → **آبی**
  - ورودی اشتباه → **قرمز**
  - راهنمایی → **سبز**
- **سیستم راهنمایی**: نمایش یک خانه خالی با یک کلیک.
- **بررسی راه‌حل**: اعتبارسنجی تخته فعلی بدون حل کامل.
- **رابط چندزبانه**: پشتیبانی کامل از **انگلیسی**، **فارسی (راست‌چین)**، **چینی** و **روسی**.
- **۵ تم زیبا**:
  - پیش‌فرض ویندوز
  - روشن
  - تاریک
  - آبی
  - قرمز
- **پشتیبانی راست‌چین**: جهت‌گیری خودکار برای فارسی.
- **تشخیص پایان بازی**: پس از ۳ اشتباه بازی تمام می‌شود.
- **جشن پیروزی**: نمایش زمان و تعداد راهنمایی‌ها پس از حل.

### پیش‌نیازها
- پایتون ۳.۸ یا بالاتر
- PyQt6

### نصب
۱. پایتون را نصب کنید.
۲. وابستگی را نصب کنید:
   ```bash
   pip install PyQt6
   ```
۳. بازی را اجرا کنید:
   ```bash
   python sudoku.py
   ```

### نحوه استفاده
- **شروع بازی**: خانه‌های خالی را با اعداد ۱ تا ۹ پر کنید.
- **انتخاب دشواری**: از آسان تا حرفه‌ای از طریق منوی کشویی.
- **دریافت راهنمایی**: روی **راهنمایی** کلیک کنید.
- **بررسی پیشرفت**: روی **بررسی** کلیک کنید.
- **بازی جدید**: هر زمان شروع تازه کنید.
- **تغییر زبان/تم**: از انتخابگرهای هدر استفاده کنید.

### تصاویر
- هدر تمیز با کنترل دشواری، زبان و تم  
- شبکه ۹×۹ پاسخگو با حاشیه‌های ضخیم بلوک‌های ۳×۳  
- رابط فارسی راست‌چین با ترجمه کامل  
- تم تاریک با وضعیت‌های ورودی پرکنتراست  
- پنجره پیروزی با آمار زمان و راهنمایی  
- شمارنده اشتباهات و نوار پیشرفت لحظه‌ای  

### نکات فنی
- **حل‌کننده بازگشتی**: تولید و حل کارآمدد پازل‌ها به‌طور مؤثر.
- **QLineEdit سفارشی**: `SudokuCell` با اعتبارسنجی، استایل و سایه.
- **تم‌بندی پویا**: کنترل کامل پالت و استایل‌شیت.
- **معماری مبتنی بر سیگنال**: جداسازی تمیز منطق و رابط.
- **مقیاس دشواری**: حذف ۴۵ تا ۶۰ خانه بر اساس سطح.
- **چندپلتفرمی**: اجرا روی ویندوز، مک و لینوکس.

### مشارکت
فورک کنید و بهبود دهید: بازگشت/جلو، علامت مداد، چالش روزانه یا خروجی PDF. Pull requestها خوش‌آمد!

### مجوز
مجوز MIT – آزاد برای استفاده شخصی، آموزشی و تجاری.

---

## 中文

### 概述
**数独 – 专业版** 是一款现代化、功能丰富的桌面数独游戏，使用 **Python** 和 **PyQt6** 构建。拥有 Windows 11 风格界面、实时验证、多语言支持、动态主题和智能谜题生成，适合休闲玩家和谜题爱好者。

### 主要功能
- **9×9 交互网格**：大尺寸响应式单元格，带**实时输入验证**和**视觉反馈**。
- **智能谜题生成器**：使用**回溯算法**生成有效、唯一谜题，支持 4 种难度。
- **实时进度追踪**：
  - **计时器** (分:秒)
  - **错误计数** (最多 3 次)
  - **平滑进度条**
- **即时反馈**：
  - 正确输入 → **蓝色**
  - 错误输入 → **红色**
  - 提示 → **绿色**
- **提示系统**：一键显示任意空单元格。
- **检查答案**：验证当前棋盘而不完成。
- **多语言界面**：完全支持 **英语**、**波斯语（RTL）**、**中文** 和 **俄语**。
- **5 种优雅主题**：
  - Windows 默认
  - 明亮
  - 暗黑
  - 蓝色
  - 红色
- **RTL 布局支持**：波斯语自动右到左。
- **游戏结束检测**：3 次错误后结束。
- **胜利庆祝**：完成时显示时间和提示使用次数。

### 要求
- Python 3.8+
- PyQt6

### 安装
1. 确保已安装 Python。
2. 安装依赖：
   ```bash
   pip install PyQt6
   ```
3. 运行游戏：
   ```bash
   python sudoku.py
   ```

### 使用方法
- **开始游戏**：用 1–9 填充空白格。
- **选择难度**：通过下拉菜单选择 简单 → 专家。
- **使用提示**：点击 **提示** 显示一格。
- **检查进度**：点击 **检查** 验证。
- **新游戏**：随时重新开始。
- **切换语言/主题**：使用顶部选择器。

### 截图
- 带难度、语言和主题控制的简洁顶部  
- 带粗线 3×3 区块边框的响应式 9×9 网格  
- 波斯语 RTL 界面，完整翻译  
- 暗黑主题，高对比度输入状态  
- 胜利对话框，显示时间和提示统计  
- 实时错误计数和进度条  

### 技术亮点
- **回溯求解器**：高效生成和求解谜题。
- **自定义 QLineEdit**：`SudokuCell` 带验证、样式和阴影。
- **动态主题**：完整调色板 + 样式表控制。
- **信号驱动架构**：逻辑与 UI 清晰分离。
- **难度分级**：根据级别移除 45–60 个单元格。
- **跨平台**：支持 Windows、macOS 和 Linux。

### 贡献
Fork 并改进：添加撤销/重做、铅笔标记、每日挑战或导出 PDF。欢迎 Pull Request！

### 许可证
MIT 许可证 – 免费用于个人、教育和商业用途。