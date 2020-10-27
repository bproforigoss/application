import Aggregate

order1 = Aggregate.OrderAggregate()
order2 = Aggregate.OrderAggregate()

sequence = ["order1.add_order_item(\"Milk\", \"2\")",
            "order1.add_order_item(\"Bread\", \"1\")",
            "order2.add_order_item(\"Nails\", \"100\")",
            "order1.add_order_item(\"Flour\", \"3\")",
            "order2.add_order_item(\"Wood plank\", \"10\")",
            "order2.add_order_item(\"Glue\", \"1\")",
            "order1.remove_order_item(\"Bread\")",
            "order1.submit_order(\"ABC\", \"Address1\")",
            "order2.submit_order(\"XYZ\", \"Address2\")",
            "order1.delete_order()"]

i = 1
for action in sequence:
    print(f"\nExecute event {i}:\n{action}")
    input("Press Enter")
    eval(action)
    i += 1

input("\nDemonstrate replay of past events, press Enter\n")
order3 = Aggregate.OrderAggregate()
order3.aggregate_id = order1.aggregate_id
order3.load_up()
