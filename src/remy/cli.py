'''The command-line parser.'''
import typer
from rich.console import Console
from rich.panel import Panel
from .core import add_recipe_from_url, generate_meal_plan
from .storage import get_recipes_dir, load_all_recipes

app = typer.Typer(help="Remy: Your local macOS meal planning assistant.")
console = Console()


@app.command()
def add(url: str = typer.Argument(..., help="URL of the recipe webpage to extract")):
    """Extract a recipe from a URL and save it to Remy's JSON library."""
    with console.status("[bold green]Fetching webpage and extracting recipe with fm..."):
        try:
            recipe, path = add_recipe_from_url(url)
        except Exception as e:
            console.print(f"[bold red]Failed to add recipe:[/bold red] {e}")
            raise typer.Exit(code=1)

    console.print(f"[bold green]Added:[/bold green] {recipe.title} ({len(recipe.ingredients)} ingredients)")
    console.print(f"[dim]Saved to {path}[/dim]")


@app.command(name="list")
def list_recipes(recipe_id: int = typer.Argument(0, help="ID number of the recipe to view")):
    """List all saved recipes in Remy's library unless an ID is provided, then just show that one."""
    recipes = load_all_recipes()
    if not recipes:
        console.print(f"No recipes saved yet in [dim]{get_recipes_dir()}[/dim]")
        return

    for idx, r in enumerate(recipes, 1):
        if recipe_id:
            if idx == recipe_id:
                console.print(f"[bold]{r.title}[/bold]")
                console.print("\n[bold]INGREDIENTS:[/bold]")
                for i in r.ingredients:
                    console.print(f"{i.quantity} {i.unit} - {i.name}")
                console.print("\n[bold]INSTRUCTIONS:[/bold]")
                for j in r.instructions:
                    console.print(f"{j}")
        else:
            console.print(f"{idx}. [bold]{r.title}[/bold] ({len(r.ingredients)} ingredients)")


@app.command()
def plan(n: int = typer.Argument(3, help="Number of meals to plan")):
    """Plan N meals and generate a grouped shopping list."""
    try:
        meals, shopping_list = generate_meal_plan(n)
    except ValueError as e:
        console.print(f"[bold yellow]{e}[/bold yellow]")
        raise typer.Exit(code=1)

    menu_lines = "\n".join(f"• {m.title}" for m in meals)
    console.print(Panel(menu_lines, title=f"Menu ({len(meals)} Meals)", border_style="green"))

    console.print("\n[bold underline]Shopping List[/bold underline]")
    for category, items in shopping_list.items():
        console.print(f"\n[bold cyan]{category}[/bold cyan]")
        for item in items:
            qty = f"{item.quantity:g} " if item.quantity is not None else ""
            unit = f"{item.unit} " if item.unit else ""
            console.print(f"  [ ] {qty}{unit}{item.name}")


if __name__ == "__main__":
    app()
