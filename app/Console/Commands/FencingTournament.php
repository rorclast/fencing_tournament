<?php

namespace App\Console\Commands;

use Storage;
use Faker;
use Illuminate\Console\Command;

class FencingTournament extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'tournament:generate {rows=50}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Generate test data for the FencingTournament problem.';

    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct()
    {
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $this->info('Starting execution.');

        $faker = Faker\Factory::create();
        $randomNumber = $faker->randomNumber();

        for ($i = 0; $i < $this->argument('rows'); $i++) {
            $lastName = $faker->lastName;
            $firstName = $faker->firstName;
            $team = strtoupper($faker->word);
            $rank = $faker->randomElement($array = ['A', 'B', 'C', 'D', 'E', 'U']);
            if ($rank !== 'U') {
                $rank .= $faker->numberBetween($min = 1, $max = 15);
            }

            $participant = [
                $lastName,
                $firstName,
                $team,
                $rank
            ];

            Storage::append(
                "tournament/participants_{$randomNumber}.csv",
                implode(',', $participant)
            );
        }

        $this->info('Ending execution.');
    }
}
