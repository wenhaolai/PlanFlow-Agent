import warnings

try:
    # 优先尝试导入新包名 ddgs
    from ddgs import DDGS
except ImportError:
    try:
        # 回退到旧包名，并忽略重命名警告
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            from duckduckgo_search import DDGS
    except ImportError:
        DDGS = None

def web_search(query: str) -> str:
    """
    使用网络搜索引擎查找信息。
    
    Args:
        query: 需要搜索的关键词或问题。
        
    Returns:
        str: 搜索结果的摘要信息。
    """
    if DDGS:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                # print(f"关于{query} 的搜索，获得信息：{results}")
                if not results:
                    return f"未找到关于 '{query}' 的结果。"
                return "\n\n".join([f"标题: {r['title']}\n链接: {r['href']}\n摘要: {r['body']}" for r in results])
        except Exception as e:
            return f"搜索出错: {str(e)}"
    else:
        # Mock implementation if library is missing
        return f"[模拟搜索结果] 关于 '{query}' 的相关信息：\n1. 这是一个模拟的搜索结果条目。\n2. 请安装 duckduckgo-search 库以启用真实搜索。"
